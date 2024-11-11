from fioer.job import FioTask
from typing import List
import numpy as np



def calc_test_slope(data: List[float]) -> float:
    """
    calculate the slope of the data
    """
    
    
def collect_task_iops(task):

    _data = task.view.output
    iops_w_mean = _data[-1]["jobs"][0]["write"]["iops_mean"]
    iops_w_max  = _data[-1]["jobs"][0]["write"]["iops_max" ]
    iops_w_min  = _data[-1]["jobs"][0]["write"]["iops_min" ]
    
    iops_r_mean = _data[-1]["jobs"][0]["read"]["iops_mean"]
    iops_r_max  = _data[-1]["jobs"][0]["read"]["iops_max" ]
    iops_r_min  = _data[-1]["jobs"][0]["read"]["iops_min" ]
    
    #iops_total = iops_r_mean+iops_w_mean
    arr_iops_read  = (iops_r_min, iops_r_max, iops_r_mean)
    arr_iops_write = (iops_w_min, iops_w_max, iops_w_mean)

    return {
        "total":iops_r_mean+iops_w_mean,
        "read" :{"max":iops_r_max, "min":iops_r_min, "mean":iops_r_mean},
        "write":{"max":iops_w_max, "min":iops_w_min, "mean":iops_w_mean}
    }




def check_tasks_convergence(tasks: List[FioTask], threshold: float = 0.01) -> bool:
    """
    check tests convergence: steady state or not
    """
    # check the slope of tasks of (x-5:x) iops data, x: final test round
    
    tasks_iops = [collect_task_iops(task) for task in tasks]

    # Sample data for x and y
    arr_x = np.array([i for i in range(len(tasks_iops))])  # replace with your data
    arr_iops = np.array(tasks_iops)  # replace with your data

    # Mean of x and y
    x_mean = np.mean(arr_x)
    iops_mean = np.mean(arr_iops)

    # calc the slope
    numerator = np.sum((arr_x - x_mean) * (arr_iops - iops_mean))
    denominator = np.sum((arr_x - x_mean) ** 2)
    slope = numerator / denominator
    
    return slope < threshold


