from pathlib import Path

from fioer.job import FioTask, PurgeTask
from fioer.log import get_logger

logger = get_logger(__name__)

# according to SNIA section 7
# fioer task based SNIA standard workflow: IOPS test

# for developing, assume the device is client-SSD which is:
# TC=2, QD=16, 



def flow_snia_iops(project_path, rwmix_mapping=None, bs_mapping=None):
    
    
    pr = Path(project_path)
    pr = pr.absolute()
    logger.info(f"Start IOPS test flow in project path: {pr}")
    
    #1. Purge
    # currently we ignore "purge" task for pocs
    # purge  = PurgeTask(...)
    logger.info("Start Purge Task: currently ignore")
    # here, assume the essential purge task has been done
    logger.info("assume purge task finished")
    
    
    # 2.2: SEQ Workload Independent Preconditioning
    # 2X capacity, 128KiB writes
    precond = FioTask(pr.joinpath("step.02.precond"))
    logger.info("start Preconditioning Task: seq write")
    precond.input.content["global"] = {
        "name":"seq",
        "rw": "write",
        "bs": "128k",
        "direct": 1,
        "ioengine":"libaio"
    }
    precond.input.content["seq_write"] = {
        "size": "128MB",# FIXME: should auto config the nvme device size
        "numjobs": 2,
        "iodepth": 16,
        "filename": "seq_write_meta",
    }
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
    
    num_tasks = len(rwmix_mapping) * len(bs_mapping)
    logger.info("start IOPs rwmix-bs mapping task...")
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
            # _tasks_round = []
            # for _round in max_round:
                
            wd_precond = FioTask(pr.joinpath(f"step03.mapping_{rwmix}-{100-rwmix}_bs_{bs}"))
            wd_precond.input.content["global"] = {
                "name":f"rwmix_bs",
                "rw": "randrw",
                "rwmixread": rwmix,
                "bs": f"{bs}k",
                "direct": 1,
                "ioengine":"libaio",
                "runtime":200, #FIXME: for test, 10s
                "time_based":1
            }
            wd_precond.input.content["rand_read_write"] = {
                "size": "10M",# FIXME: owing to the volume prob, just use 10M foLSr test
                "numjobs": 2,
                "iodepth": 16,
                "filename": "randrw_meta",
            }
            # for every 1s, print the status
            wd_precond.run(cli_params={"status-interval": "1"})
            logger.info(f"IOPs rwmix-bs mapping task: rwmix-{rwmix}/{100-rwmix} bs-{bs} finished")
            
            #TODO convergence check
            #_res = check_convergence(tasks_round)
            # if converged, then break
            # get iops-(bs, rwmix) data
    
    # TODO: reporting
    
    return 




#MISC

# from fioer.visualize import _load_json

# def collect_job_data(task):

#     _data = _load_json(task.view.output)
#     iops_r_mean = _data[-1]["jobs"][0]["write"]["iops_mean"]
#     iops_w_mean = _data[-1]["jobs"][0]["read" ]["iops_mean"]
#     iops_total = iops_r_mean+iops_w_mean
    
#     return iops_total