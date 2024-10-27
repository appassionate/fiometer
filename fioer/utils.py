import configparser
import json
import os

from io import StringIO

# add return type


def ini2dict(ini_text: str) -> dict:
    """ini text to dict

    Args:
        ini_text (str): ini text

    Returns:
        _type_: dict
    """

    config = configparser.ConfigParser()
    config.read_file(StringIO(ini_text))

    config_dict = {section: dict(config.items(section)) for section in config.sections()}
    return config_dict


def dict2ini(config_dict):
    """_summary_

    Args:
        config_dict (_type_): ini/fio.ini configuration dict

    Returns:
        _type_: int text for output
    """

    config = configparser.ConfigParser()
    for section, options in config_dict.items():
        config[section] = options

    with StringIO() as f:
        config.write(f, space_around_delimiters=False)
        ini_text = f.getvalue()

    return ini_text


def process_json_timestamp(json_text: str):
    """ proecess un-formatted json output from fio

    Args:
        json_text (str): _description_

    Returns:
        _type_: _description_
    """

    json_text = '[' + json_text.replace('}\n{', '},{') + ']'
    json_data = json.loads(json_text)

    return json_data


def find_executable(cmd):
    """using which to find executable directory, only for linux
    """
    # linux: which command to find executable
    result = os.subprocess.run(f'which {cmd}', shell=True, check=True)
    executable = result.stdout

    # TODO: verify the executable is a directory

    return executable
