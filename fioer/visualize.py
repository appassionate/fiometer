from pathlib import Path

from pydantic import BaseModel
import numpy as np
import json
import matplotlib.pyplot as plt

_DPI = 600
LATENCY_TYPE = ("slat", "clat", "lat")


def cumsum(array):
    return np.cumsum(array) / np.arange(1, len(array) + 1)

def _load_json(file):
    
    with open(file, "r") as f:
        data = json.load(f)
    return data

def _create_fig():
    return plt.subplots(figsize=(10, 3), dpi=_DPI)

class FioView(BaseModel):
    
    
    work_path: str = ""
    file_output: str = "parsed.json"
    
    def _load_job_info(self, job):
        self.work_path = job.work_path

    @property
    def output(self):
        return str(Path(self.work_path).joinpath(self.file_output).absolute())

    def view_latency(self, mode="write", lat_type="lat", job_num=0, ax=None):
        """_summary_

        Args:
            mode (_type_): write/read/randwrite/randread
            lat_type (str, optional): latency: submission-lat/compliment-lat/total-lat. Defaults to "lat" as total-lat.
            job_num (int, optional): which job to view. Defaults to index: 0
            ax (_type_, optional): ax for overview or other fig, ax pair, Defaults to None

        Raises:
            ValueError: _description_

        Returns:
            _type_: fig, ax of matplotlib
        """
        
        output = _load_json(self.output)
        
        if lat_type not in LATENCY_TYPE:
            raise ValueError(f"latency type not supported: {lat_type}")
        
        lenframe = len(output)
        collect_lat_ns_mean = [ _frame["jobs"][job_num][mode][f"{lat_type}_ns"]["mean"] for _frame in output]
        collect_cum_lat_ns_mean = cumsum(collect_lat_ns_mean)
        # ns trans to μs array
        collect_lat_mean = np.array(collect_lat_ns_mean) / 1000
        collect_cum_lat_mean = np.array(collect_cum_lat_ns_mean) / 1000
        
        
        #fig, ax
        if not ax:
            fig, ax = plt.subplots(figsize=(10, 3),dpi=_DPI)
        else:
            fig = ax.get_figure()
        
        # plot
        ax.plot(range(len(output)), collect_lat_mean, label=f"{lat_type}_mean", color="b")
        ax.plot(range(len(output)), collect_cum_lat_mean, label=f"{lat_type}_mean_cum", color="r")
        
        # add title and labels
        ax.set_title(f"{mode.upper()}: Latency: {lat_type.upper()} Over {lenframe} Frames")
        ax.set_xlabel("Time (Frame)")
        ax.set_ylabel("Latency (μs)")
        
        # show grid and legend
        ax.grid(True)
        ax.legend()
        
        
        #grid setting: "--"
        ax.grid(True, linestyle='--')
        
        plt.show()
        
        return fig, ax

    def view_iops(self, mode, job_num=0, ax=None):
        """ view one job iops over frames

        Args:
            mode (_type_): write/read/randwrite/randread
            job_num (int, optional): which job to view. Defaults to index: 0
            ax (_type_, optional): ax for overview or other fig, ax pair, Defaults to None

        Returns:
            _type_: fig, ax of matplotlib
        """        
        
        output = _load_json(self.output)
        lenframe = len(output)

        collect_iops_mean = [frame["jobs"][0][mode]["iops"] for frame in output]
        collect_iops = [frame["jobs"][0][mode]["iops_mean"] for frame in output]

        # traj[0]["jobs"][0]["write"]["iops_min"]
        # traj[0]["jobs"][0]["write"]["iops_max"]

        # traj[0]["jobs"][0]["write"]["iops_stddev"]
        # traj[0]["jobs"][0]["write"]["iops_samples"]

        # fig, ax
        if not ax:
            fig, ax = plt.subplots(figsize=(10, 3), dpi=_DPI)
        else:
            fig = ax.get_figure()

        # plot iops
        ax.plot(range(len(output)), collect_iops_mean,
                label="iops_mean", color="b")
        ax.plot(range(len(output)), collect_iops, label="iops", color="r")

        # add title and labels
        ax.set_title(f"{mode.upper()}: IOPS Over {lenframe} Frames")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("IOPS")

        # show grid and legend
        ax.grid(True)
        ax.legend()

        # ax.set_xlim(0,100)
        # ax.set_ylim(0,1000000)

        # grid setting: "--"
        ax.grid(True, linestyle='--')

        # show
        plt.show()
        return fig, ax


    def overview_latency(self, mode="write", lat_type="lat", dpi=300):
        """overview latency of all jobs

        Args:
            mode (_type_): write/read/randwrite/randread
            job_num (int, optional): which job to view. Defaults to index: 0
            dpi (int, optional): _description_. Defaults to 300.

        Returns:
            _type_: fig, ax of matplotlib 
        """        

        # graph: overview, contains n*1 sub-graphs
        output = _load_json(self.output)
        job_num = len(output[0]["jobs"])
        fig, axs = plt.subplots(job_num, 1, figsize=(10, 2 * job_num), dpi=_DPI, gridspec_kw={'hspace': 1})

        # avoiding subscriptable error
        if job_num == 1:
            axs = [axs]
        for i, ax in enumerate(axs):
            self.view_latency(mode=mode, lat_type=lat_type, job_num=i, ax=ax)

        return fig, axs
    
    
    def overview_iops(self, mode="write", dpi=300):
        """overview iops of all jobs

        Args:
            mode (_type_): write/read/randwrite/randread
            dpi (int, optional): _description_. Defaults to 300.

        Returns:
            _type_: fig, ax of matplotlib
        """        
        
        # TODO: cache the output json data, load once
        # TODO: dpi imple

        # graph: overview, contains n*1 sub-graphs
        output = _load_json(self.output)
        job_num = len(output[0]["jobs"])
        fig, axs = plt.subplots(job_num, 1, figsize=(10, 2 * job_num), dpi=_DPI, gridspec_kw={'hspace': 1})

        # avoiding subscriptable error
        if job_num == 1:
            axs = [axs]
        for i, ax in enumerate(axs):
            self.view_iops(mode=mode, job_num=i, ax=ax)

        return fig, axs
