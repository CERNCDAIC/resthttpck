#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import os
import time
from datetime import datetime
from datetime import timedelta

from base.RestLogger import RestLogger
from threading import Thread
from base.MySQLDB import MySQLDB
from base.Utils import Utils


class QueryWorker(Thread):

    def __init__(self, pathtoqueries, timetosleep, writelogspath, fromtime, host, port, username, password, db, charset):
        Thread.__init__(self)
        self.pathtoqueries = os.path.normpath(pathtoqueries)
        self.fromtime = fromtime
        self.writelogspath = writelogspath
        dbtype, self.namelog = os.path.basename(os.path.normpath(pathtoqueries)).split('-')
        if dbtype == 'mysql':
            self.mysqldb = MySQLDB(host, port, username, password, db, charset)
        self.sleep = timetosleep

    def run(self):
        while True:
            RestLogger.debug("Fromtime is <{}>".format(self.fromtime.strftime('%Y-%m-%d %H-%M-%S')))
            rows = self.mysqldb.selectstmts(self.pathtoqueries, self.fromtime.strftime('%Y-%m-%d %H-%M-%S'))
            if self._is2DList(rows):
                for arr in rows:
                    Utils.AppendToFile(Utils.GenerateNameFile(self.writelogspath, self.namelog, '%Y%m%d'), arr)
            else:
                Utils.AppendToFile(Utils.GenerateNameFile(self.writelogspath, self.namelog, '%Y%m%d'), rows)
            time.sleep(self.sleep * 60)
            self.fromtime = datetime.today() - timedelta(minutes=self.sleep)

    def _is2DList(self, matrix_list):
        if matrix_list:
            if isinstance(matrix_list[0], list):
                return True
        return False

