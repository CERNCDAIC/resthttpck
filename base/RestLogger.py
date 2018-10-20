#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import logging
import logging.config
import json
import os


class RestLogger:
    logger = None

    def __init__(self, name='resthttpck', logconfig='/etc/resthttpck/logging.conf'):
        if os.path.exists(logconfig):
            with open(logconfig) as jdata:
                config_logging = json.load(jdata)
                logging.config.dictConfig(config_logging)

            RestLogger.logger = logging.getLogger(name)
    @classmethod
    def debug(cls, string):
        cls.logger.debug(string)

