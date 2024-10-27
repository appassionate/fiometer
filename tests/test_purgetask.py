import unittest
import shutil

import pytest
from pathlib import Path

import fioer
from fioer.job import PurgeTask

_WORK_PATH = '/tmp/fioer/test/'
_TEMPLATE_DIR = Path(fioer.__file__).joinpath('../../templates').resolve()



class TestPurgeTask(unittest.TestCase):
    
    def test_purgetask_init(self):
        """purge task init(create) test"""
        
        _purge = PurgeTask(
            work_path=_WORK_PATH+"test_purge_init",
            input_dict={},
        )
        _purge.input.content["device"] = "/dev/XXXXXXXXXX"
        _purge.write_input()
        
        # file exists
        self.assertTrue(Path(_purge.get_file_directory("input.json")).exists())
        self.assertTrue(Path(_purge.get_file_directory("output")).exists())
        
    def test_purgetask_run(self):
        """ purge task run test"""
        
        _purge = PurgeTask(
            work_path=_WORK_PATH+"test_purge_run",
            input_dict={},
        )
        
        _purge.run()
        
        
        # file exists
        self.assertTrue(Path(_purge.get_file_directory("input.json")).exists())
        self.assertTrue(Path(_purge.get_file_directory("output")).exists())
        # _purge._load_workpath()
        # self.assertTrue(_purge.status == "done")
        