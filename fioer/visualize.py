from pathlib import Path
import copy
from typing import Optional

from pydantic import BaseModel, Field, PrivateAttr
import numpy as np
import json
import matplotlib.pyplot as plt
from .log import get_logger

_DPI = 600
LATENCY_TYPE = ("slat", "clat", "lat")

logger = get_logger(__name__)

class ViewCache():
    data = {}
    def _clean(self):
        self.data = {}
    
#singleton for cache output, avoid pydantic lock

def cumsum(array):
    return np.cumsum(array) / np.arange(1, len(array) + 1)

def _load_json(file):
    
    with open(file, "r") as f:
        data = json.load(f)
    return data

def _create_fig():
    return plt.subplots(figsize=(10, 3), dpi=_DPI)


def _create_fig_both():
    fig, axs = plt.subplots(2, 1, figsize=(10, 2 * 2), dpi=_DPI, gridspec_kw={'hspace': 0.7})
    return fig, axs

def _draw_jobnum_text(ax, job_name, job_num, total_num):
    
    # add text : top-left, 
    ax.set_title(f"job: {job_name}, No. {job_num}/{total_num}", loc="left", fontsize=12, color="black")
    pass

def get_job_names(output):
    jobnames = [job["jobname"] for job in output[0]["jobs"]]
    return list(set(jobnames))


#currently output and view are coupled
class FioView(BaseModel):
    
    
    work_path: Optional[str] = Field(None, exclude=True)
    file_output: str = "parsed.json"
    
    _cache: dict = PrivateAttr(default_factory=dict)
    
    def _load_job_info(self, job):
        self.work_path = job.work_path

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        self._cache = {}
        

    @property
    def output(self):
        
        if "output" in self._cache:
            return self._cache["output"]
        # cache output data
        output_dir = Path(self.work_path).joinpath(self.file_output).absolute()
        if not output_dir.exists():
            raise FileNotFoundError(f"file not found: {output_dir}")
        with open(output_dir, "r") as f:
            data = json.load(f)
        logger.debug(f"loaded output once from {output_dir}.")
        self._cache["output"] = data
        
        return self._cache["output"]
    
    def _reload_output(self):
        output_dir = Path(self.work_path).joinpath(self.file_output).absolute()
        if not output_dir.exists():
            raise FileNotFoundError(f"file not found: {output_dir}")
        with open(output_dir, "r") as f:
            data = json.load(f)
        logger.debug(f"reloaded output from {output_dir}.")
        self._cache["output"] = data
        
        return self._cache["output"]

    @property
    def job_names(self):
        output = self.output
        return get_job_names(output)
    
    def filter_output_by_name(self, job_name=None):
        
        if not job_name:
            job_name = self.job_names[0]
            logger.info(f"job_name not specified, using the first job name: {job_name}")
            logger.info(f"valid job names: {self.job_names}")
        # TODO: deepcopy will be slow
        _output = copy.deepcopy(self.output)
        for frame in _output:
            frame["jobs"] = [job for job in frame["jobs"] if job["jobname"] == job_name]

        return _output
    
    def get_job_dataframe(self, mode="read",job_name=None, job_num=0):
        
        import pandas as pd
        output = self.filter_output_by_name(job_name)
        frames = [ _frame["jobs"][job_num][mode] for _frame in output]
        
        return pd.DataFrame(frames)
    
    
    #TODO: can view the by jobname and jobnum
    def view_latency(self, mode="write", lat_type="lat", job_name=None, job_num=0, ax=None):
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
        
        if mode=="both":
            fig, axs = _create_fig_both()
            self.view_latency(mode="write", lat_type=lat_type, job_num=job_num, ax=axs[0])
            self.view_latency(mode="read" , lat_type=lat_type, job_num=job_num, ax=axs[1])
            return fig, axs
        
        output = self.output
        output = self.filter_output_by_name(job_name)
        
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
        
        #color setting
        if mode == "write":
            _color = "b"
        elif mode == "read":
            _color = "r"
        # plot
        ax.plot(range(len(output)), collect_lat_mean, label=f"{lat_type}_mean", color=_color)
        ax.plot(range(len(output)), collect_cum_lat_mean, label=f"{lat_type}_mean_cum", color=_color, alpha=0.2)
        
        # add title and labels
        ax.set_title(f"{mode.upper()}: Latency (μs): {lat_type.upper()} Over {lenframe} Frames")
        _draw_jobnum_text(ax, job_name, job_num+1, len(output[0]["jobs"]))
        
        ax.set_xlabel("Time (Frame)")
        ax.set_ylabel("Latency (μs)")
        
        # show grid and legend
        ax.grid(True)
        ax.legend()
        
        #grid setting: "--"
        ax.grid(True, linestyle='--')
        #add extra text
        
        return fig, ax

    def view_iops(self, mode, job_name=None, job_num=0, ax=None, show_title=True):
        """ view one job iops over frames

        Args:
            mode (_type_): write/read/both
            job_num (int, optional): which job to view. Defaults to index: 0
            ax (_type_, optional): ax for overview or other fig, ax pair, Defaults to None

        Returns:
            _type_: fig, ax of matplotlib
        """
        
        if mode=="both":
            fig, axs = _create_fig_both()
            self.view_iops(mode="write", job_name=job_name, job_num=job_num, ax=axs[0])
            self.view_iops(mode="read",  job_name=job_name, job_num=job_num, ax=axs[1])
            return fig, axs
        
        output = self.output
        output = self.filter_output_by_name(job_name)
        lenframe = len(output)

        collect_iops_mean = [frame["jobs"][job_num][mode]["iops"] for frame in output]
        collect_iops = [frame["jobs"][job_num][mode]["iops_mean"] for frame in output]

        # traj[0]["jobs"][0]["write"]["iops_min"]
        # traj[0]["jobs"][0]["write"]["iops_max"]

        # traj[0]["jobs"][0]["write"]["iops_stddev"]
        # traj[0]["jobs"][0]["write"]["iops_samples"]

        # fig, ax
        if not ax:
            fig, ax = plt.subplots(figsize=(10, 3), dpi=_DPI)
        else:
            fig = ax.get_figure()

        #color setting
        if mode == "write":
            _color = "b"
        elif mode == "read":
            _color = "r"
        # plot iops
        ax.plot(range(len(output)), collect_iops, label="iops", color=_color)
        ax.plot(range(len(output)), collect_iops_mean, label="iops_mean", color=_color, alpha=0.2)

        # add title and labels
        if show_title:
            ax.set_title(f"{mode.upper()}: IOPS (IOs/sec) Over {lenframe} Frames")
            _draw_jobnum_text(ax, job_name, job_num+1, len(output[0]["jobs"]))
        
        ax.set_xlabel("Time (Frame)")
        ax.set_ylabel("IOPS (IOs/sec)")

        # show grid and legend
        ax.grid(True)
        ax.legend()

        # ax.set_xlim(0,100)
        # ax.set_ylim(0,1000000)

        # grid setting: "--"
        ax.grid(True, linestyle='--')



        return fig, ax

    def view_bw(self, mode, job_name=None, job_num=0, ax=None, show_title=True):
        """ view one job bandwidth over frames

        Args:
            mode (_type_): write/read/both
            job_num (int, optional): which job to view. Defaults to index: 0
            ax (_type_, optional): ax for overview or other fig, ax pair, Defaults to None

        Returns:
            _type_: fig, ax of matplotlib
        """
        
        #FIXME: HOW TO SUPPORT BOTH MODE?
        
        if mode=="both":
            fig, axs = _create_fig_both()
            self.view_bw(mode="write", job_name=None, job_num=job_num, ax=axs[0])
            self.view_bw(mode="read",  job_name=None, job_num=job_num, ax=axs[1])
            return fig, axs
        
        output = self.output
        output = self.filter_output_by_name(job_name)
        lenframe = len(output)

        collect_bw_mean = [frame["jobs"][0][mode]["bw"] for frame in output]
        collect_bw = [frame["jobs"][0][mode]["bw_mean"] for frame in output]

        # fig, ax
        if not ax:
            fig, ax = plt.subplots(figsize=(10, 3), dpi=_DPI)
        else:
            fig = ax.get_figure()

        # color setting
        if mode == "write":
            _color = "b"
        elif mode == "read":
            _color = "r"
        # plot iops
        ax.plot(range(len(output)), collect_bw, label="bw", color=_color)
        ax.plot(range(len(output)), collect_bw_mean,
        label="bw_mean", color=_color, alpha=0.2)

        # add title and labels
        if show_title:
            ax.set_title(f"{mode.upper()}: Bandwidth (KB/s) Over {lenframe} Frames")
            _draw_jobnum_text(ax, job_name, job_num+1, len(output[0]["jobs"]))
        ax.set_xlabel("Time (Frame)")
        ax.set_ylabel("Bandwidth (KB/s)")

        # show grid and legend
        ax.grid(True)
        ax.legend()

        # ax.set_xlim(0,100)
        # ax.set_ylim(0,1000000)

        # grid setting: "--"
        ax.grid(True, linestyle='--')

        return fig, ax


    def view_iops_bw(self, mode, job_name=None, job_num=0, ax=None):
        """ view one job iops and bandwidth over frames

        Args:
            mode (_type_): write/read/both
            job_num (int, optional): which job to view. Defaults to index: 0
            ax (_type_, optional): ax for overview or other fig, ax pair, Defaults to None

        Returns:
            _type_: fig, ax of matplotlib
        """
        # fig, ax
        fig, ax = plt.subplots(1, 2, figsize=(10, 3), dpi=_DPI, gridspec_kw={'hspace': 1,"wspace": 0.3}) 
        self.view_bw(mode=mode, job_name=job_name, job_num=job_num, ax=ax[0],show_title=False)
        self.view_iops(mode=mode, job_name=job_name, job_num=job_num, ax=ax[1],show_title=False)

        return fig, ax
        

        
    # #BUG: job_name not implemented
    # def overview_latency(self, mode="write", lat_type="lat", dpi=300):
    #     """overview latency of all jobs

    #     Args:
    #         mode (_type_): write/read/randwrite/randread
    #         job_num (int, optional): which job to view. Defaults to index: 0
    #         dpi (int, optional): _description_. Defaults to 300.

    #     Returns:
    #         _type_: fig, ax of matplotlib 
    #     """        

    #     # graph: overview, contains n*1 sub-graphs
    #     output = self.output
    #     job_num = len(output[0]["jobs"])
    #     fig, axs = plt.subplots(job_num, 1, figsize=(10, 2 * job_num), dpi=_DPI, gridspec_kw={'hspace': 1})

    #     # avoiding subscriptable error
    #     if job_num == 1:
    #         axs = [axs]
    #     for i, ax in enumerate(axs):
    #         self.view_latency(mode=mode, lat_type=lat_type, job_num=i, ax=ax)

    #     return fig, axs
    
    
    # def overview_iops(self, mode="write", dpi=300):
    #     """overview iops of all jobs

    #     Args:
    #         mode (_type_): write/read/randwrite/randread
    #         dpi (int, optional): _description_. Defaults to 300.

    #     Returns:
    #         _type_: fig, ax of matplotlib
    #     """        
        
    #     # TODO: dpi imple

    #     # graph: overview, contains n*1 sub-graphs
    #     output = self.output
    #     job_num = len(output[0]["jobs"])
    #     fig, axs = plt.subplots(job_num, 1, figsize=(10, 2 * job_num), dpi=_DPI, gridspec_kw={'hspace': 1})

    #     # avoiding subscriptable error
    #     if job_num == 1:
    #         axs = [axs]
    #     for i, ax in enumerate(axs):
    #         self.view_iops(mode=mode, job_num=i, ax=ax)

    #     return fig, axs
