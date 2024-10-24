import os
import subprocess
import json
from pathlib import Path

from .wrapper import FioWrapper
from .input import Input
from .utils import process_json_timestamp

class JobBase():
    
    work_path: str = None
    #TODO:refactor executable later
    executable: str 
    input: Input = Input()
    
    def write_input_file(self):
        raise NotImplementedError('run method is not implemented in base')
    
    def run():
        raise NotImplementedError('run method is not implemented in base')
    
    pass

#TODO: refactor to FioTask
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
    
    def process_output_json(self):
        #parse output.json
        with open(Path(self.work_path) / "output.json", 'r') as f:
            output = f.read()
        parsed = process_json_timestamp(output)
        with open(Path(self.work_path) / "parsed.json", 'w') as f:
            json.dump(parsed, f, indent=2)
    
    
    def run(self, cli_params=None):
        
        print("--run fio task--")
        print("current input.fio:")
        print(self.input.render_dict())
        
        self.write_input_file()
        # using fio wrapper to run the job

        if not cli_params:
            cli_params = {}
        # TODO: here still consider the normal log output
        # for it will remained the interrupted log
        format_type = "json" 
        if format_type=="json":
            # set output file format: json, need test
            cli_params['output-format'] = 'json'
            cli_params['output'] = 'output.json'
        
        fio = FioWrapper(work_path=str(self.work_path), 
                         fio_binary=self.executable, 
                         config_file="input.fio")
        fio.run(cli_params=cli_params,output_file=None, error_file=None)
        
        if format_type=="json":
            self.process_output_json()
        
        print("--fio task done--")


# add an abstraction of PurgeTask
# PurgeTask will remove the disk(very dangerous) to the "FOB" state according to the SNIA standard
# using the linux nvme-cli tool to implement the feature
#ref: https://askubuntu.com/questions/1310338/how-to-secure-erase-a-nvme-ssd

class PurgeTask(JobBase):
    
    def __init__(self, work_path, input_dict, **kwargs):
        
        self.work_path = str(Path(work_path).absolute())
        self.input.content = input_dict
        self.executable = "nvme"
        
    def write_input_file(self):
        # create work_dir if not exists
        pass
    
    def run(self, cli_params=None):
        pass