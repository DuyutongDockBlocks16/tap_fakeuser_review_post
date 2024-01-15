# @Time : 2021/9/28 14:44
# @Author : xx
# @File : logger.py
# @Desc:

from logbook import Logger, FileHandler, TimedRotatingFileHandler
import time
import os

global LOG

BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
LOG_DIR = os.path.join(BASE_DIR, 'log')

''' 获取logger '''
def get_logger(logname, is_timed_rotating=True, log_dir=LOG_DIR):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logfile = os.path.join(log_dir, logname + '.log')
    if is_timed_rotating:
        TimedRotatingFileHandler(logfile, date_format='%Y%m%d', bubble=True).push_application()
    else:
        FileHandler(logfile).push_application()
    return Logger(logname)

def init():
    global LOG
    LOG = get_logger('cookie_create')

init()