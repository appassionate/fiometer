import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def cumsum(array):
    return np.cumsum(array) / np.arange(1, len(array) + 1)


LATENCY_TYPE = ("slat", "clat", "lat")


def show_latency(output:dict, type=""):
    
    if type not in LATENCY_TYPE:
        raise ValueError(f"latency type not supported: {type}")
    
    lenframe = len(output)
    collect_lat_ns_mean = [ _frame["jobs"][0]["write"][f"{type}_ns"]["mean"] for _frame in output]
    collect_cum_lat_ns_mean = cumsum(collect_lat_ns_mean)
    # ns trans to μs array
    collect_lat_mean = np.array(collect_lat_ns_mean) / 1000
    collect_cum_lat_mean = np.array(collect_cum_lat_ns_mean) / 1000
    
    
    # 使用fig, ax的方式来创建matplotlib图
    fig, ax = plt.subplots(figsize=(10, 3),dpi=600)
    
    # 绘制折线图
    ax.plot(range(len(output)), collect_lat_mean, label=f"{type}_mean", color="b")
    ax.plot(range(len(output)), collect_cum_lat_mean, label=f"{type}_mean_cum", color="r")
    
    # 添加标题和标签
    ax.set_title(f"WRITE: {type.upper()} Latency Changes Over {lenframe} Frames")
    ax.set_xlabel("Time (Frame)")
    ax.set_ylabel("Latency (μs)")
    
    # 显示网格和图例
    ax.grid(True)
    ax.legend()
    
    #grid setting: "--"
    ax.grid(True, linestyle='--')
    
    plt.show()
    
    return fig, ax



def show_iops(output:dict, ):
    
    
    ## GRAPH2: IOPS

    collect_iops_mean = [frame["jobs"][0]["write"]["iops"] for frame in traj]
    collect_iops      = [frame["jobs"][0]["write"]["iops_mean"] for frame in traj]


    # traj[0]["jobs"][0]["write"]["iops_min"]
    # traj[0]["jobs"][0]["write"]["iops_max"]

    # traj[0]["jobs"][0]["write"]["iops_stddev"]
    #traj[0]["jobs"][0]["write"]["iops_samples"]

    # 使用fig, ax的方式来创建matplotlib图
    fig, ax = plt.subplots(figsize=(10, 3),dpi=600)

    # 绘制折线图
    ax.plot(range(100), collect_iops_mean, label="iops_mean", color="b")
    ax.plot(range(100), collect_iops     , label="IOPS", color="r")

    # 添加标题和标签
    ax.set_title("WRITE: IOPS Over 100 Seconds")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("IOPS")

    # 显示网格和图例
    ax.grid(True)
    ax.legend()

    #
    # ax.set_xlim(0,100)
    # ax.set_ylim(0,1000000)

    #grid setting: "--"
    ax.grid(True, linestyle='--')

    # 显示图像
    plt.show()

