from pathlib import Path

from fioer.job import FioTask, PurgeTask
from fioer.log import get_logger

logger = get_logger(__name__)

# according to SNIA section 7
# fioer task based SNIA standard workflow: IOPS test

# for developing, assume the device is client-SSD which is:
# TC=2, QD=16,not sure :(



def flow_snia_iops(project_path, device_path=None, rwmix_mapping=None, bs_mapping=None, mode_rw="seqrw", as_file=True):
    """_summary_

    Args:
        project_path (_type_): flow project path
        device_path (_type_): device or directory path
        rwmix_mapping (_type_, optional): _description_. Defaults to None.
        bs_mapping (_type_, optional): _description_. Defaults to None.
        mode_rw (str, optional): seqrw/randrw. Defaults to "seqrw".

    Raises:
        ValueError: _description_
    """
    
    pr = Path(project_path)
    pr = pr.absolute()
    
    if device_path is None:
        logger.warning("[WARNING] just for test, using project path as device path")
        device_path = pr.joinpath("file_meta")
    else:
        device_path = Path(device_path)
        # 
    
    logger.info(f"Start IOPS test flow in project path: {pr}")
    logger.info(f"device path: {device_path}")
    
    #1. Purge
    # currently we ignore "purge" task for pocs
    # purge  = PurgeTask(...)
    logger.info("Start Purge Task: currently ignore")
    # here, assume the essential purge task has been done
    logger.info("assume purge task finished")
    
    
    # 2.2: SEQ Workload Independent Preconditioning
    # 2X capacity, 128KiB writes
    precond = FioTask(pr.joinpath("02.precond"), input_dict={})
    logger.info("start Preconditioning Task: seq write")
    precond.input.content["global"] = {
        "name":"precond",
        "rw": "write",
        "bs": "128k",
        "direct": 1,
        "ioengine":"libaio"

    }
    
    # size should be auto determined by /dev/xxx 100%,  loops=2 
    precond.input.content["seq_write"] = {
        "size": "128MB",# FIXME: should auto config the nvme device size
        "numjobs": 1,
        # "iodepth": 16,
        "filename": f"{device_path}",
    }
    ### FIXME 
    if not as_file:
        precond.input.content["seq_write"]["size"] = "100%"
        precond.input.content["seq_write"]["loops"] = 2
    ### 
    
    
    precond.run()
    logger.info(f"Preconditioning Task finished")
    
    # 3.1: Workload Dependent Preconditioning: test params
    # data pattern: random
    # value mapping:
    # R/W mix: 100/0, 95/5, 65/35, 50/50, 35/65, 5/95, 0/100
    # block size: 0.5KiB, 4KiB, 8KiB, 16KiB, 32KiB, 64KiB, 128KiB, 1024KiB
    # rwmix_mapping = [100, 95, 65, 50, 35, 5, 0]
    # bs_mapping = [0.5, 4, 8, 16, 32, 64, 128, 1024]
    
    #for test 
    # rwmix_mapping = [0,50,100]
    # bs_mapping = [4, 8]
    
    if mode_rw == "seqrw":
        mode_rw = "rw"
    if mode_rw == "randrw":
        mode_rw = "randrw"
        
    MAX_CONVERGE_ROUND = 6
    
    num_tasks = len(rwmix_mapping) * len(bs_mapping)
    logger.info("start IOPs rwmix-bs mapping task...")
    logger.info(f"current rw mode: {mode_rw}")
    logger.info(f"rwmix_mapping: {rwmix_mapping}")
    logger.info(f"bs_mapping: {bs_mapping}")
    logger.info(f"total tasks: {num_tasks}")
    
    _count = 0
    for rwmix in rwmix_mapping:
        for bs in bs_mapping:
            _count += 1
            logger.info(f"mapping task progress: {_count}/{num_tasks}")
            logger.info(f"start IOPs rwmix-bs mapping task: rwmix-{rwmix}/{100-rwmix} bs-{bs}")
            
            # TODO: converge task resume
            # max round set to 25, if not converge, then stop
            _tasks_round = []
            for _round in range(MAX_CONVERGE_ROUND):
                
                #BUG: input dict still have pointer problem
                wd_precond = FioTask(pr.joinpath(f"03.mapping-rwmix{rwmix}-bs{bs}/round-{_round}"),input_dict={})
                wd_precond.input.content["global"] = {
                    "name":f"rwmix_bs",
                    "rw": f"{mode_rw}", #seqrw for test  (rw/randrw)
                    "rwmixread": rwmix,
                    "bs": f"{bs}k",
                    "direct": 1,
                    "ioengine":"libaio", # modified here maybe convient to test other ioecd ..ngine
                    "runtime": 60, # SNIA standard: 60s
                    "time_based":1
                }
                wd_precond.input.content["read_write"] = {
                    "size": "10M",# FIXME: owing to the volume prob, just use 10M foLSr test
                    "numjobs": 1, #set to 1 
                    "iodepth": 16,
                    "filename": f"{device_path}",
                }
                
                # for every 1s, print the status
                wd_precond.run(cli_params={"status-interval": "1"})
                logger.info(f"IOPs rwmix-bs mapping task: rwmix-{rwmix}/{100-rwmix} bs-{bs} finished")
                
                #TODO convergence check
                #_res = check_convergence(tasks_round)
                # if converged, then break
                # get iops-(bs, rwmix) data
    
    # TODO: reporting
    print("currently finished")
    plot_graph_bs_rwmix(pr, bs_mapping, rwmix_mapping)
    
    return 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fioer.flow.utils import collect_task_iops

def plot_graph_bs_rwmix(pr, bs,rwmix):
    
    # data for plot
    # bs = [0.5, 4, 8, 16, 32, 64, 128, 1024]
    # rwmix = [0,50,100]

    #collect data scheme
    arr_iops = np.empty((len(bs), len(rwmix)), dtype=np.float32)
    for i,_bs in enumerate(bs):
        for j, _rwmix in enumerate(rwmix):
            _task = FioTask(pr.joinpath(f"03.mapping-rwmix{_rwmix}-bs{_bs}/round-5"))
            _data = collect_task_iops(_task)
            arr_iops[i, j] = _data["total"]
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    xpos, ypos = np.meshgrid(np.arange(len(bs)), np.arange(len(rwmix)), indexing="ij")
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)
    dz = arr_iops.flatten()
    dx = dy = 0.5
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='skyblue', edgecolor='k')

    ax.set_xlabel('Block Size (KiB)')
    ax.set_ylabel('R/W Mix (%)')
    ax.set_zlabel('IOPS')

    ax.set_xticks(np.arange(len(bs)))
    ax.set_xticklabels(bs)
    ax.set_yticks(np.arange(len(rwmix)))
    ax.set_yticklabels(rwmix)

    plt.show()
    
    return
