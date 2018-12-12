#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import argparse
import os
import time
from datetime import datetime
from datetime import timedelta


from base.MySQLDB import MySQLDB
from base.RestLogger import RestLogger
from config import APPCONFIG
from base.Utils import Utils

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processing of tasks')
    parser.add_argument('--path', action='store', type=str, dest='sqlpath', required=False,
                        help='sqlstatements to execute in a directory')
    parser.add_argument('--file', action='store', type=str, dest='sqlfile', required=False,
                        help='sqlstatement to execute in a file')
    parser.add_argument('--from', action='store', type=str, dest='fromtime', required=False,
                        help='from where to start to look for')
    parser.add_argument('--sleeptime', action='store', type=int, dest='sleeptime', required=False, default=10,
                        help='how often to run the loop in secs')


    results = parser.parse_args()
    RestLogger(name='resthttpck', logconfig='/etc/resthttpck/logging.conf')

    RestLogger.debug(parser.parse_args())

    if not results.fromtime:
        results.fromtime = datetime.today() - timedelta(hours=1)


    host, port, username, password, db, charset = APPCONFIG['vidyo']['mysql_db'].split(':')
    mysqldb = MySQLDB(host, port, username, password, db, charset)
    if results.sqlpath and os.path.exists(results.sqlpath):
        while True:
            rows = mysqldb.selectstmts(results.sqlpath, results.fromtime.strftime('%Y-%m-%d %H-%M-%S'))
            Utils.AppendToFile(Utils.GenerateNameFile(APPCONFIG['vidyo']['sqllogs'], "cdraccess", '%Y%m%d'), rows)
            time.sleep(results.sleeptime)
            results.fromtime = datetime.today() - timedelta(minutes=results.sleeptime)





