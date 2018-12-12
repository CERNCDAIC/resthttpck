#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import pymysql
from prettytable import PrettyTable
from base.Utils import Utils
from base.RestLogger import RestLogger

class MySQLDB:

    def __init__(self, host, port, user, password, db, charset):
        self.connection = pymysql.connect(host=host,
                                     user=user,
                                     port=int(port),
                                     password=password,
                                     db=db,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor)


    def selectstmt(self, sql, *params):
        with self.connection.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            RestLogger.debug("The query affected {} rows".format(cursor.rowcount))
            # get tuple with names of columns
            desc = cursor.description
            fullrows = []
            for r in result:
                row = [r[name[0]] for name in desc]
                fullrows.append(','.join(map(str, row)))
            return fullrows


    def selectstmts(self, path, *params):
        sqlfiles = Utils.ListOfFiles(path)
        allrows = []
        for f in sqlfiles:
            RestLogger.debug("Working with sql file: {}".format(f))
            sql = Utils.ReadFile(f)
            RestLogger.debug("sql is {}".format(sql))
            result = self.selectstmt(sql, *params)
            if result:
                allrows.append(result)
        RestLogger.debug("In total, {} rows".format(sum(len(x) for x in allrows)))
        return allrows


