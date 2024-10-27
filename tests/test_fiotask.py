import unittest
import shutil
from pathlib import Path

import fioer
from fioer.job import FioTask
import pytest
# from pytest_dependency import depends


_WORK_PATH = '/tmp/fioer/test/'
_TEMPLATE_DIR = Path(fioer.__file__).joinpath('../../templates').resolve()


#test fioer.job.FioTask
class TestFioTask(unittest.TestCase):
    
    
    def test_fiotask_init(self):
        """fio task init(create) test"""
        
        _fio = FioTask(
            work_path=_WORK_PATH+"test_fio_init",
            input_dict={},
        )
        _fio.input.from_input_file(_TEMPLATE_DIR.joinpath('example.fio'))
        _fio.write_input()
        
        # file exists
        self.assertTrue(Path(_fio.get_file_directory("input.fio")).exists())
        self.assertTrue(Path(_fio.get_file_directory(".fioer_info.json")).exists())


    def test_fiotask_run(self):
        """ fio task run test"""
        
        _fio = FioTask(
            work_path=_WORK_PATH+"test_fio_run",
            input_dict={},
        )
        _fio.input.from_input_file(_TEMPLATE_DIR.joinpath('example.fio'))
        _fio.run()
        
        # file exists
        self.assertTrue(Path(_fio.get_file_directory("input.fio")).exists())
        self.assertTrue(Path(_fio.get_file_directory(".fioer_info.json")).exists())
        self.assertTrue(Path(_fio.get_file_directory("output.json")).exists())
        self.assertTrue(Path(_fio.get_file_directory("parsed.json")).exists())
        _fio._load_workpath()
        self.assertTrue(_fio.status == "done")

        self._fio_run  = _fio
        
        return _fio
    
    
    # def test_fiotask_reload(self):
    #     """fio task reload existing .json info"""
        
    #     # should after test-run
    #     #test-run 
    #     _fio = FioTask(work_path=_WORK_PATH+"test_fio_run",)
    #     print(_fio.status)
    #     self.assertTrue(_fio.status == "done")
    
    #     #TODO: more reload in different way
