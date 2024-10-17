import configparser
import json
import os

from io import StringIO


def ini2dict(ini_text):
    
    config = configparser.ConfigParser()
    config.read_file(StringIO(ini_text))
    
    config_dict = {section: dict(config.items(section)) for section in config.sections()}
    return config_dict

def dict_to_ini(config_dict):
    
    config = configparser.ConfigParser()
    for section, options in config_dict.items():
        config[section] = options

    with StringIO() as f:
        config.write(f)
        ini_text = f.getvalue()


    return ini_text

def generate_fio_input_file(fio_input_file, fio_input):
    with open(fio_input_file, 'w') as f:
        f.write(json.dumps(fio_input, indent=4))
        

def find_executable():
    # linux: which command to find executable
    os.subprocess.run('which fio', shell=True, check=True)
    
    pass