#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import argparse
import re
import os

import base.Sorenson
import base.Vidyo
import base.MySQLDB
from base.Utils import Utils
from base.RestLogger import RestLogger
from base.Httpbase import Httpbase
from config import APPCONFIG

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processing of tasks')
    parser.add_argument('--c', action='store', type=str, dest='classtest', required=True, default='Sorenson',
                        help='Sorenson test')
    parser.add_argument('--t', action='store', type=str, dest='whichtest', required=True, default=None,
                        help='type of job to be sent e.g. Sorenson:transcoding ')
    parser.add_argument('--n', action='store', type=int, dest='numberofjobs', required=False, default=1,
                        help='how many of whichtest jobs to be sent')


    results = parser.parse_args()
    RestLogger(name='resthttpck', logconfig='/etc/resthttpck/logging.conf')

    RestLogger.debug(parser.parse_args())

    host, port, username, password, db, charset = APPCONFIG['vidyo']['mysqldb']

    mysqldb = base.MySQLDB(host, port, username, password, db, charset)
