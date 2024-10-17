import configparser
import json
import os

from io import StringIO


def ini2dict(ini_text):
    
    config = configparser.ConfigParser()
    config.read_file(StringIO(ini_text))
    
    config_dict = {section: dict(config.items(section)) for section in config.sections()}
    return config_dict

def dict2ini(config_dict):
    
    config = configparser.ConfigParser()
    for section, options in config_dict.items():
        config[section] = options

    with StringIO() as f:
        config.write(f, space_around_delimiters=False)
        ini_text = f.getvalue()


    return ini_text


def process_json_timestamp(json_text:str):
    
    json_text = '[' + json_text.replace('}\n{', '},{') + ']'
    json_data = json.loads(json_text)
    
    return json_data


def find_executable():
    # linux: which command to find executable
    os.subprocess.run('which fio', shell=True, check=True)
    
    pass