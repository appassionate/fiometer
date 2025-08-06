import os
import logging

level_name = os.environ.get('LOG_LEVEL', 'INFO')
level = logging._nameToLevel.get(level_name, logging.INFO)

logging.basicConfig(
    level=level,
    format="%(asctime)s - %(name)-25s - %(levelname)-8s - %(message)s",
    datefmt="%m-%d %H:%M",
    # filename="fiometer.log",
    # filemode="w",
)


def get_logger(name=None):
    return logging.getLogger(name)