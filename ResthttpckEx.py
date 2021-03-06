#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

class ResthttpckEx(Exception):
    def __init__(self, message, http_error_code):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.http_error_code = http_error_code