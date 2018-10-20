#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import os
import random
import re
import time

from base.RestLogger import RestLogger

class Utils:

    @staticmethod
    def ReadFile(path):
        data = []
        if os.path.exists(path):
            with open(path, 'r') as myfile:
                data = myfile.read()
        return data

    @staticmethod
    def GivemeOne(arr):
        if arr:
            return random.choice(arr)
        return

    @staticmethod
    def FindAll(regex, str):
        regexall = []
        if regex:
            regexobj = re.compile(regex, re.MULTILINE)
            regexall = regexobj.findall(str)
        return regexall

    @staticmethod
    def ReplaceStr(regex, str, replacement):
        result = None
        if regex:
            regexobj = re.compile(regex, re.MULTILINE)
            result = regexobj.sub(replacement, str)
        return result

    @staticmethod
    def GenerateName(prefix):
        import string
        allchar = string.ascii_letters + string.digits
        random_string = "".join(random.choice(allchar) for x in range(1, 6))
        return '{}_{}'.format(prefix, random_string)

    @staticmethod
    def CreateEmptyFile(path):
        with open(path, 'a'):
            os.utime(path, None)

    @staticmethod
    def FilesYoungerthan(path, hours):
        current_time = time.time()
        arr_files = []
        for f in os.listdir(path):
            creation_time = os.path.getctime(os.path.join(path,f))
            if (current_time - creation_time) < (hours * 3600):
                arr_files.append(f)
                RestLogger.debug("{} fulfills criteria".format(f))
        return arr_files
