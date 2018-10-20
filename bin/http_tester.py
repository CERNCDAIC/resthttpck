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
from base.Utils import Utils
from base.RestLogger import RestLogger
from base.Httpbase import Httpbase
from config import APPCONFIG

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processing of tasks')
    parser.add_argument('--c', action='store', type=str, dest='classtest', required=True, default='Sorenson',
                        help='Sorenson test')
    parser.add_argument('--t', action='store', type=str, dest='whichtest', required=True, default=None,
                        help='type of job to be sent, Sorenson:transcoding ')
    parser.add_argument('--n', action='store', type=int, dest='numberofjobs', required=False, default=1,
                        help='how many of whichtest jobs to be sent')


    results = parser.parse_args()
    RestLogger(name='resthttpck', logconfig='/etc/resthttpck/logging.conf')

    RestLogger.debug(parser.parse_args())

    # Let's create a job for Sorenson
    class_obj = None
    filepath = None
    if results.classtest.casefold() == "sorenson":
        classname = "Sorenson"
        sorenson_class = getattr(base.Sorenson, classname)
        class_obj = sorenson_class()
        # which test can have any name from Sorenson class public methods e.g. transcoding_job
        # parameters can be encoded like transcoding_job_true

        transcoding_job_pattern = re.compile(r'^transcoding_job(_True|_False)?(_.*)?$')
        if transcoding_job_pattern.search(results.whichtest):
            tuple_groups = transcoding_job_pattern.search(results.whichtest).groups()
            single = False
            title = "No title given"
            if tuple_groups[0]:
                single = tuple_groups[0].replace('_', '')
                if single == 'False':
                    single = False
                else:
                    single = True
            if tuple_groups[1]:
                title = tuple_groups[1].replace('_', '')

            RestLogger.debug("single: {} title: {} selected.".format(single, title))

            filepath = class_obj.transcoding_job(title, single)
            json_struct = class_obj.PostSorenson(filepath)
            RestLogger.debug("Jobid: {} title: {} submitted.".format(json_struct['JobId'], title))
            Utils.CreateEmptyFile(os.path.join(APPCONFIG['general']['jobidfiles'], json_struct['JobId']))
        else:
            RestLogger.debug("No transcoding job")

        query_job_pattern = re.compile(r'^query_job_(\d+)?(_.*)?$')
        if query_job_pattern.search(results.whichtest):
            tuple_groups = query_job_pattern.search(results.whichtest).groups()
            timing = 1
            status_job = "default"
            if tuple_groups[0]:
                timing = tuple_groups[0].replace('_', '')
            if tuple_groups[1]:
                status_job = tuple_groups[1].replace('_', '')
            response = class_obj.query_job(timing, status_job)
            RestLogger.debug(response)
        else:
            RestLogger.debug("Not a query job")

    # send the job


