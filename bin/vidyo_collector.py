#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import argparse
from datetime import datetime
from datetime import timedelta


from base.QueryWorker import QueryWorker
from base.CleanUpWorker import CleanUpWorker
from base.RestLogger import RestLogger
from config import APPCONFIG


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processing of tasks')
    parser.add_argument('--path', action='store', type=str, dest='sqlpaths', required=False,
                        help='sqlstatements to execute in a directory')
    parser.add_argument('--file', action='store', type=str, dest='sqlfile', required=False,
                        help='sqlstatement to execute in a file')
    parser.add_argument('--from', action='store', type=str, dest='fromtime', required=False,
                        help='from where to start to look for')
    parser.add_argument('--sleeptime', action='store', type=int, dest='sleeptime', required=False, default=10,
                        help='how often to run the loop in minutes')
    parser.add_argument('--cleanup', action='store', type=int, dest='cleanup', required=False, default=0,
                        help='How many days logs files are kept')

    results = parser.parse_args()
    RestLogger(name='resthttpck', logconfig='/etc/resthttpck/logging.conf')

    RestLogger.debug(parser.parse_args())

    if not results.fromtime:
        results.fromtime = datetime.today() - timedelta(hours=1)

    threads = []
    for p in results.sqlpaths.split(':'):
        RestLogger.debug('Checking path <{}>'.format(p))
        if 'mysql' in p and 'vidyo' in p:
            host, port, username, password, db, charset = APPCONFIG['vidyo']['mysql_db'].split(':')
            sqllogpath = APPCONFIG['vidyo']['sqllogs']
        else:
            RestLogger.debug("Wrong path name, please include provider e.g. vidyo and type of db e.g. 'mysql' ")
            continue
        thread = QueryWorker(p, results.sleeptime, sqllogpath, results.fromtime, host, port,
                             username, password, db, charset)
        threads += [thread]
        thread.start()
    if results.cleanup:
        thread = CleanUpWorker(APPCONFIG['vidyo']['sqllogs'], 10 * results.sleeptime, results.cleanup)
        threads += [thread]
        thread.start()

    for x in threads:
        x.join()





