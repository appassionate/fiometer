import os
import subprocess
from pathlib import Path

from .wrapper import FioWrapper
from .input import Input

class JobBase():
    
    work_path: str = None
    #TODO:refactor executable later
    executable: str 
    input: Input = Input()
    
    def write_input_file(self):
        raise NotImplementedError('run method is not implemented yet')
    
    def run():
        raise NotImplementedError('run method is not implemented yet')
    
    pass


class Job(JobBase):
    
    def __init__(self, work_path, input_dict, **kwargs):
        
        self.work_path = str(Path(work_path).absolute())
        self.input.content = input_dict
        self.executable = "fio"
        
    def write_input_file(self):
        # create work_dir if not exists
        Path(self.work_path).mkdir(parents=True, exist_ok=False)
        with open(Path(self.work_path) / "input.fio", 'w') as f:
            f.write(self.input.render_dict())
    
    def run(self, cli_params=None):
        
        
        self.write_input_file()
        # using fio wrapper to run the job
        fio = FioWrapper(work_path=str(self.work_path), 
                         fio_binary=self.executable, 
                         config_file="input.fio")
        fio.run(cli_params=cli_params,output_file="output", error_file="error")
        