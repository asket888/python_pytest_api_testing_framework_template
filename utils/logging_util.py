import logging
from os import path
from logging.config import fileConfig

_PATH_TO_LOGIN_CONFIG = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'logging.ini')
fileConfig(_PATH_TO_LOGIN_CONFIG)
logger = logging.getLogger()
