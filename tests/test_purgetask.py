import unittest
import shutil

import pytest
from pathlib import Path

import fiometer
from fiometer.job import PurgeTask

_WORK_PATH = '/tmp/fiometer/test/'
_TEMPLATE_DIR = Path(fiometer.__file__).joinpath('../../templates').resolve()


@pytest.fixture
def setup_work_directory():
    """Fixture to set up and clean up the work directory before each test."""

    _purge = PurgeTask(
        work_path=_WORK_PATH + "test_purge_init",
        input_dict={},
    )
    return _purge

def test_purgetask_init(setup_work_directory):
    """Test initializing (creating) a PurgeTask"""

    _purge = setup_work_directory
    _purge.input.content["device"] = "/AAAAAAAAAAAAA/BBBBBBBBBBBBBBBBBBB"
    _purge.write_input()

    # Check that the input file exists
    assert Path(_purge.get_file_directory("input.json")).exists()


# def test_purgetask_run(setup_work_directory):
#     """Test running a PurgeTask"""

#     _purge = setup_work_directory
#     _purge.input.content["device"] = "/AAAAAAAAAAAAA/BBBBBBBBBBBBBBBBBBB"
#     _purge.write_input()
#     _purge.run()

#     # Check that the input and output files exist
#     assert Path(_purge.get_file_directory("input.json")).exists()
#     assert Path(_purge.get_file_directory("output")).exists()

