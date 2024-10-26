import subprocess
from .log import get_logger

logger = get_logger(__name__)

class FioWrapper:
    def __init__(self, work_path=".", fio_binary='fio', config_file="input.fio"):
        
        self.fio_binary = fio_binary
        self.config_file = config_file
        self.work_path = work_path


    def run(self, cli_params=None, output_file=None, error_file=None):
        """
        执行 fio，传递 CLI 参数和配置文件。
        
        :param cli_params: 传递给 fio 的命令行参数，字典形式。
        :param output_file: 如果指定，fio的输出将重定向到该文件中。
        :return: 返回 fio 执行的输出。
        """
        if not self.config_file:
            raise ValueError("No fio config file specified or created")

        # base command
        command = f"{self.fio_binary} {self.config_file}"

        # add cli params
        if cli_params:
            for key, value in cli_params.items():
                command += f' --{key}={value}'
        
        
        # output,error file
        if output_file:
            command += f" > {output_file}"
        if error_file:
            command += f" 2> {error_file}"
        
        logger.info(f"current work path: {self.work_path}")
        logger.info(f"executing fio command: {command}")

        # 执行命令
        with subprocess.Popen(command, shell=True, 
                              cwd=self.work_path, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True) as proc:
            
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                raise RuntimeError(f"fio failed with error:\n{stderr}")
            
            # save subprocess output to file

            return stdout
