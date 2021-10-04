"""This module provides the tools for logging in PyAnsys"""

# The approach is to call ``Getlogger``` at the beginning of each module.
# Functions in several ways:
# * If ``GetLogger`` gets called before any other logger has been initialized, it will create
# the default logger which parameters are a constant in this module.
# * If ``GetLogger`` gets called after another logger has been created, there are two options:
#    * If we do not intend changes in the messages format, it will return a child logger with
# the default name. This child logger will redirect all the output to the main.
#    * If we do intend changes in the message format because maybe we want to account for
# different context, a new child logger is created with the same handlers as the parent and
# using the providen message format or the parent message format.
#
# In cases we want to change the format according to different contexts, for example when the
# module launcher is called by the pool module:
#
# >

import logging

LOG_LEVEL = logging.DEBUG
CONSOLE_MSG_FORMAT = '%(funcName)s - %(message)s'
FILE_MSG_FORMAT = '%(asctime)s - %(module)s:%(funcName)s- %(message)s'
FILE_NAME = 'pyansys.log'

CONSOLE_MSG_POOL_FORMAT = '%(threadName)s: %(module)s: %(funcName)s - %(message)s'
FILE_MSG_POOL_FORMAT = '%(asctime)s - %(threadName)s: %(module)s: %(funcName)s - %(message)s'


def getLogger(name=None, file_msg=None, console_msg=None, fname=None, loglevel=LOG_LEVEL):
    logger = logging.getLogger(name)

    if logger.parent.hasHandlers():

        if file_msg is None and console_msg is None and logger.parent.name != 'pool':
            # We are not going to change the message output, hence we can reuse the whole logger.
            return logger

        ## There is a previous logger used
        # Since there is no easy way to modify the format at a given logger, we just create a new one (logger)
        # and pass the same file and stream handlers as the parent one, giving the option for change the format.
        fh = [each_handler for each_handler in logger.parent.handlers if isinstance(each_handler, logging.FileHandler)][0]
        ch = [each_handler for each_handler in logger.parent.handlers if isinstance(each_handler, logging.StreamHandler)][0]

        if logger.parent.name == 'pool':
            fh.setFormatter(logging.Formatter(file_msg or FILE_MSG_POOL_FORMAT))
            ch.setFormatter(logging.Formatter(console_msg or CONSOLE_MSG_POOL_FORMAT))

        else:
            fh.setFormatter(logging.Formatter(file_msg or fh.formatter._fmt))
            ch.setFormatter(logging.Formatter(console_msg or ch.formatter._fmt))

        logger.propagate = False

    else:
        # There is no parent logger, so we create it.
        logger.setLevel(loglevel)
        fh = logging.StreamHandler()
        ch = logging.FileHandler(fname or FILE_NAME)

        fh.setFormatter(logging.Formatter(file_msg or FILE_MSG_FORMAT))
        ch.setFormatter(logging.Formatter(console_msg or CONSOLE_MSG_FORMAT))
        logger.propagate = True  # Probably this is irrelevant.

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
