import pytest
from fioer.job import FioTask
from pathlib import Path
import fioer

_WORK_PATH = '/tmp/fioer/test/'
_TEMPLATE_DIR = Path(fioer.__file__).joinpath('../../templates').resolve()
_SAMPLE_DIR = Path(fioer.__file__).joinpath('../../tests/samples').resolve()



@pytest.fixture
def setup_fiotask():
    _fio = FioTask(
        work_path=_WORK_PATH+"randrw65",
        input_dict={},
    )
    return _fio


#@pytest.mark.parametrize
def test_fioview_view(setup_fiotask):
    
    _fio = setup_fiotask

    _fio.view.view_iops(mode="write", job_name="file1", job_num=0, ax=None)
    _fio.view.view_iops(mode="read",  job_name="file1", job_num=0, ax=None)

    _fio.view.view_latency(mode="write", job_name="file1", job_num=0, ax=None)
    _fio.view.view_latency(mode="read",  job_name="file1", job_num=0, ax=None)

    _fio.view.view_iops_bw(mode="write",  job_name="file1", job_num=0, ax=None)
    _fio.view.view_iops_bw(mode="read",   job_name="file1", job_num=0, ax=None)