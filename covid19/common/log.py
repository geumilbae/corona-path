import logging
import logging.handlers
import os
import sys
import time


"""Tools related with logging.

This module provides customized Logger object with structured formats and I/O.

Example:
    from .log import LoggerFactory
    ...
    mylogger = LoggerFactory('logger name').logger

Attributes:
    DEFAULT_FORMAT_STRING (str): default logging format.
    DICT_LEVEL (dict)

Todo:
    * allow to customize logger easily.
"""
ROOT_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


DEFAULT_FORMAT_STRING = \
    '[%(levelname)s|%(module)s|%(funcName)s|:%(lineno)d]' + \
    '%(asctime)s>%(message)s'


DICT_LEVEL = {
    'DEBUG': logging.DEBUG,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
}


def _construct_log_file_name(name: str):
    now = time.localtime()
    ymd = f"{now.tm_year:04d}{now.tm_mon:02d}{now.tm_mday:02d}"
    # hms = f"{now.tm_hour:02d}{now.tm_min:02d}{now.tm_sec:02d}"
    log_file_name = f"{name}_{ymd}.log"
    return log_file_name


def _construct_formatter(format_string: str):
    formatter = logging.Formatter(format_string)
    return formatter


def _construct_stream_handler(
        formatter: logging.Formatter, level: str):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(DICT_LEVEL[level.upper()])
    stream_handler.setFormatter(formatter)
    return stream_handler


def _construct_file_handler(file_path: str,
                            formatter: logging.Formatter,
                            level: str):
    file_handler = logging.handlers.RotatingFileHandler(
        filename=file_path,
        maxBytes=10*1024*1024,
        backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(DICT_LEVEL[level.upper()])
    return file_handler


def _construct_logger(name: str,
                      stream_handler: logging.StreamHandler,
                      file_handler: logging.FileHandler,
                      level: str):
    logger = logging.getLogger(name)
    logger.setLevel(DICT_LEVEL[level.upper()])
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


class LoggerFactory:
    """LoggerFactory constructs and provides customized logger
    in initialization. There is no required parameters in __init__()
    but recommend using unique name. It will be in the log file name.

    Args:
        name (str, optional)
        format_string (str, optional)
        level (str, optional)

    Attributes:
        _log_file_path (str)
        _logger (logging.Logger)
    """

    def __init__(self,
                 name: str = 'default',
                 format_string: str = DEFAULT_FORMAT_STRING,
                 level: str = 'DEBUG'):
        log_file_name = _construct_log_file_name(name)
        self._log_file_path = os.path.join(ROOT_DIR, 'log', log_file_name)
        formatter = _construct_formatter(format_string)
        file_handler = _construct_file_handler(
            self._log_file_path, formatter, level)
        stream_handler = _construct_stream_handler(formatter, level)
        self._logger = _construct_logger(
            name, stream_handler, file_handler, level)

    @property
    def logger(self):
        self._logger.handlers[0].stream = sys.stdout
        return self._logger
