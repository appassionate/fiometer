import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

## GRAPH1: latency_ns:total

# collect_lat_ns_min  = [ _frame["jobs"][0]["write"]["lat_ns"]["min"] for _frame in traj]
# collect_lat_ns_max  = [ _frame["jobs"][0]["write"]["lat_ns"]["max"] for _frame in traj]
# collect_lat_ns_stddev = [ _frame["jobs"][0]["write"]["lat_ns"]["stddev"] for _frame in traj]

collect_lat_ns_mean = [ _frame["jobs"][0]["write"]["lat_ns"]["mean"] for _frame in traj]
collect_cum_lat_ns_mean = np.cumsum(collect_lat_ns_mean) / np.arange(1, len(collect_lat_ns_mean) + 1)

# fig, ax style
fig, ax = plt.subplots(figsize=(10, 3),dpi=600)

# 绘制折线图
ax.plot(range(100), collect_lat_ns_mean, label="lat_ns_mean", color="b")
ax.plot(range(100), collect_cum_lat_ns_mean, label="lat_ns_mean_cum", color="r")

# add title and axis
ax.set_title("WRITE: Mean Latency Changes Over 100 Seconds")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Latency (ns)")

ax.grid(True)
ax.legend()

ax.set_xlim(0,100)
ax.set_ylim(0,1000000)

#grid setting: "--"
ax.grid(True, linestyle='--')

plt.show()



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
