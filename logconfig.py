# -*- coding:utf-8 -*-


import os
import logging
import time
from logging import handlers
from app_path import base_dir


class Logger(object):
    level_relations = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self,  level='info', when='D', back_Count=3,
                 fmt='%(asctime)s %(pathname)s[%(lineno)d] - %(levelname)s: %(message)s'):

        day = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        file_dir = os.path.join(base_dir,"log")
        filename = os.path.join(file_dir, (day + '.log'))
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_Count, encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


logger = Logger(level="DEBUG").logger
# logger.info(f"sysdict{sysdict}")
# logger.info(f"hasforzen{hasforzen}")