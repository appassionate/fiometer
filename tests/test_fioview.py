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
        work_path=_SAMPLE_DIR.joinpath("randrw65"),
        input_dict={},
    )
    return _fio


# test job_num, lat_type 

@pytest.mark.parametrize("mode, lat_type", [
    ("write", "clat"),
    ("write", "slat"),
    ("write", "lat" ),
    ("read", "lat" ),
    ("read", "lat" ),
    ("read", "lat" ),
])
def test_fioview_view(setup_fiotask, mode, lat_type):
    
    _fio = setup_fiotask
    _fio.view.view_latency(mode=mode, job_name="file1", job_num=0, lat_type=lat_type, ax=None)