import pytest
from pathlib import Path
import shutil
import unittest

import fiometer
from fiometer.job import FioTask

_WORK_PATH = '/tmp/fiometer/test/'
_TEMPLATE_DIR = Path(fiometer.__file__).joinpath('../../templates').resolve()


@pytest.fixture
def setup_fiotask():
    
    _fio = FioTask(
        work_path=_WORK_PATH+"test_fio_run",
        input_dict={},
    )
    return _fio

def test_fiotask_init(setup_fiotask):
    """fio task init(create) test"""
    
    _fio = setup_fiotask
    _fio.input.from_input_file(_TEMPLATE_DIR.joinpath('example.fio'))
    _fio.write_input()
    
    # file exists
    assert Path(_fio.get_file_directory("input.fio")).exists()
    assert Path(_fio.get_file_directory(".fiometer_info.json")).exists()
    

def test_fiotask_run(setup_fiotask):
    """fio task run test"""
    
    _fio = setup_fiotask
    _fio.input.from_input_file(_TEMPLATE_DIR.joinpath('example.fio'))
    _fio.run()
    
    # file exists
    assert Path(_fio.get_file_directory("input.fio")).exists()
    assert Path(_fio.get_file_directory(".fiometer_info.json")).exists()
    assert Path(_fio.get_file_directory("output.json")).exists()
    assert Path(_fio.get_file_directory("parsed.json")).exists()
    _fio._load_workpath()
    assert _fio.status == "done"
    
    return _fio

def test_fiotask_input():
    
                    
    fio_a = FioTask(
    work_path=_WORK_PATH+"input_a",
    )
    fio_a.input.content["aaa"] = "aaa"

    fio_b = FioTask(
    work_path=_WORK_PATH+"input_b",
    )
    assert fio_a.input.content is not fio_b.input.content