# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 10:46:01 2016

@author: Lathropk
"""
import os
import datetime
import logging
from django.conf import settings


class ExtractLogger:
    logger = None
    def myLogger(self):
        if None == self.logger:
            self.logger=logging.getLogger('Extract')
            self.logger.setLevel(logging.DEBUG)
            now = datetime.datetime.now()
            # if using windows, use '\' rather than '/'
            log_file = os.path.join(settings.PROJECT_DIR,
                                    'logs/extract_'+ now.strftime("%Y-%m-%d") +'.log')
            handler=logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self.logger


class TransformLogger:
    logger = None
    def myLogger(self):
        if None == self.logger:
            self.logger=logging.getLogger('Transform')
            self.logger.setLevel(logging.DEBUG)
            now = datetime.datetime.now()
            log_file = os.path.join(settings.PROJECT_DIR,
                                    'logs/transform_'+ now.strftime("%Y-%m-%d") +'.log')
            handler=logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self.logger


class UpdateElasticLogger:
    logger = None
    def myLogger(self):
        if None == self.logger:
            self.logger=logging.getLogger('ElasticUpdate')
            self.logger.setLevel(logging.DEBUG)
            now = datetime.datetime.now()
            log_file = os.path.join(settings.PROJECT_DIR,
                                    'logs/elastic_update_'+ now.strftime("%Y-%m-%d") +'.log')
            handler=logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self.logger
