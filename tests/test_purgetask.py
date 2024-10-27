import unittest
import shutil

import pytest
from pathlib import Path

import fioer
from fioer.job import PurgeTask

_WORK_PATH = '/tmp/fioer/test/'
_TEMPLATE_DIR = Path(fioer.__file__).joinpath('../../templates').resolve()


#test fioer.job.FioTask

# class TestPurgeTask(unittest.TestCase)