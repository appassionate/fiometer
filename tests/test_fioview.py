import pytest
from fioer.job import FioTask
from pathlib import Path
import fioer

_WORK_PATH = '/tmp/fioer/test/'
_TEMPLATE_DIR = Path(fioer.__file__).joinpath('../../templates').resolve()
_SAMPLE_DIR = Path(fioer.__file__).joinpath('../../samples').resolve()

#@pytest.mark.parametrize