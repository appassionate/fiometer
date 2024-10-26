import os
import logging

level_name = os.environ.get('LOG_LEVEL', 'INFO')
level = logging._nameToLevel.get(level_name, logging.INFO)

logging.basicConfig(format='%(asctime)s %(name)s: %(message)s', level=level)
logging.getLogger('transitions.core').setLevel(logging.WARNING)

def get_logger(name=None):
    return logging.getLogger(name)