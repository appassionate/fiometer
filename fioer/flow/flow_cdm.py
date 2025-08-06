from pathlib import Path

from fiometer.job import FioTask, PurgeTask
from fiometer.log import get_logger

logger = get_logger(__name__)



# following crystal disk mark test setting
def flow_cdm(project_path, file_path,
             file_size="1G", repeat=5, time_interval=5,
             
             ):
    
    
    # 4 main tasks in CDM test
    # 1. SEQ, 1M  , Q8 , T1
    # 2. SEQ, 128K, Q32, T1
    # 3. RND, 4K  , Q32, T16
    # 4. RND, 4K  , Q1 , T1
    
    pr = Path(project_path)
    
    logger.info(f"Start CDM test flow in project path: {pr}")
    
    #step1: read
    
    _setting = {"rw": "seq", "bs": "1m", "q": 8, }
    
    tasks_read = []
    _read_1mq8t1    = FioTask(pr.joinpath("01.seq_1m_q8_t1"), input_dict={})    
    _read_128kq32t1 = FioTask(pr.joinpath("02.seq_128k_q32_t1"), input_dict={})
    
    
    #step2: write
    
    
    _job = FioTask(pr.joinpath("01.seq_1m_q8_t1"), input_dict={})
    #balabala