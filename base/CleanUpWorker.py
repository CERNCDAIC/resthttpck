#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2019, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import os
import time

from base.RestLogger import RestLogger
from threading import Thread

class CleanUpWorker(Thread):

    def __init__(self, directory, timetosleep, age):
        Thread.__init__(self)
        self.pathtocleanup = directory
        # in minutes
        self.sleep = timetosleep
        # days to be kept, converted to secs
        self.age = int(age) * 86400

    def run(self):
        while True:
            RestLogger.debug("Clean-up of logs files older than {} secs".format(self.age))
            now = time.time()
            for file in os.listdir(self.pathtocleanup):
                fullpath = os.path.join(self.pathtocleanup, file)
                modified = os.stat(fullpath).st_mtime
                if modified < (now - self.age):
                    if os.path.isfile(fullpath):
                        os.remove(fullpath)
                        RestLogger.debug("Removing {}".format(fullpath))
            time.sleep(self.sleep * 60)
