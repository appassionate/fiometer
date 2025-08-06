# fiometer
python wrapper and default test settings for fio, ssd-test oriented

[中文](./README_CN.md)/[English](./README.md)

## example 
### 1. random read/write example

```python
from fiometer.job import FioTask

template_file = "bala/randrw.fio"

randrw = FioTask(work_path="./randrw",input_dict=None,)
randrw.input.from_input_file(template_file)
randrw.run(cli_params={"status-interval":"1"})
```

template: randrw.fio
r/w = 65/35
```ini
[global]
name=fio-rand-write
filename=fio-rand-write
rw=randrw
bs=4K
direct=1
numjobs=1
time_based=1
runtime=200
ioengine=libaio
iodepth=64
rwmixread=65

[file1]
size=10M

```


## SNIA-PTS PARAMETER TABLE
according to SNIA-PTS, section 2.1.1 

| SNIA  | FIO  | Description |
| --- | --- | --- |
| `blocksize` | `bs` | block size |
| `Read/Write` | `randrw(rwmixread=X)` | read/write |
| `OIO: Outstanding IO,/( Queue Depth)` | `iodepth` | iodepth |
| `Thread Count(Workers, Process)` | `numjobs` | number of jobs |
| `Latency` | `slat, clat, lat` | latency |
| `Cache` | `direct=1` | direct IO |



## data visualization
from data(parsed.json)

```python
randrw.view.view_iops(mode="write")
randrw.view.view_latency(mode="write", lat_type="lat")
```
or both plotted
```python
randrw.view.view_iops(mode="both")
randrw.view.view_latency(mode="both", lat_type="lat")
```

## SNIA IOPs test flow(developing)
accroding to snia pts psedo code
```python
from fiometer.flow import flow_snia_iops
flow_snia_iops(project_path="./wf",rwmix_mapping=[0,35,50,65,100], bs_mapping=[4,8,16,32])
```

### flow folder abstract
every tasks in flow will be placed in determined folder, like below:
```shell
tree ./wf
```

```shell
.
├── 02.precond
│   ├── input.fio
│   ├── output.json
│   ├── parsed.json
│   └── seq_write_meta
├── 03.mapping-rwmix0-bs16
│   ├── round-0
│   │   ├── input.fio
│   │   ├── output.json
│   │   ├── parsed.json
│   │   └── rw_meta
│   ├── round-1
│   │   ├── input.fio
│   │   ├── output.json
│   │   ├── parsed.json
│   │   └── rw_meta
```

3d graph draft:
<div >
    <img src="./images/flow_sina_poc.png" alt="Description" width="400">
    <img src="./images/log.png" alt="Description" width="700">
</div>



## other visualize example

gfio style:
![iops_bw_r](./images/iops_bw_r.png) 
![iops_bw_w](./images/iops_bw_w.png)

iops: read/write both plotted
![iops](./images/iops_rw.png)
latency: read/write both plotted
![latency](./images/lat_rw.png)
latency per job:
![latency-total](./images/lat_perjob.png)


### TODO LIST
1. write amplification flow/test-case
2. snia standard flow/test-case
3. QoS flow/test-case