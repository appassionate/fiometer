import subprocess

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

        # 基础命令
        command = [self.fio_binary, self.config_file]

        # 添加 CLI 参数
        if cli_params:
            for key, value in cli_params.items():
                command.append(f' --{key}={value} ')
        
        if output_file:
            command.append(f" > {output_file}")
        if error_file:
            command.append(f" 2> {error_file}")
        print(f"Executing fio command: {' '.join(command)}")

        # 执行命令
        with subprocess.Popen(command, shell=True, cwd=self.work_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            stdout, stderr = proc.communicate()
            print("current work path:", self.work_path)
            if proc.returncode != 0:
                raise RuntimeError(f"fio failed with error:\n{stderr}")
            
            # save subprocess output to file

            return stdout
