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
from ResthttpckEx import ResthttpckEx
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
    # possible values for Vidyo are:
    # CreatePublicRoom:True:True:True, ToggleRoomProfile:85589:NoAudioAndVideo, GetRoomProfile:123132
    # possible values for Sorenson are:
    # transcoding_job_False or transcoding_job_True
    # query_job_1
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
    elif results.classtest.casefold() == "vidyo":
        classname = "Vidyo"
        vidyo_class = getattr(base.Vidyo, classname)
        username = APPCONFIG['vidyo']['username']
        password = APPCONFIG['vidyo']['password']

        m = re.match(r'CreatePublicRoom(:(True|False))?(:(True|False))?(:(True|False))?',
                    results.whichtest,
                    re.IGNORECASE)
        if m:
            wsdl = APPCONFIG['vidyo']['admin_wsdl']
            class_obj = vidyo_class(username, password, wsdl)
            islocked = False
            hasPIN = False
            hasmoderatorPIN = False
            if m.group(2):
                islocked = True
            if m.group(4):
                hasPIN = True
            if m.group(6):
                hasmoderatorPIN = True
            getattr(class_obj, 'CreatePublicRoom')(name=Utils.GenerateName("Vidyo_resthttpck_api"),
                                                  owner=APPCONFIG['vidyo']['owner'],
                                                  islocked=islocked,
                                                  hasPIN=hasPIN,
                                                  hasmoderatorPIN=hasmoderatorPIN)

        m = re.match(r'ToggleRoomProfile(:\d+)(:\w+)?',
                    results.whichtest,
                    re.IGNORECASE)
        if m:
            wsdl = APPCONFIG['vidyo']['admin_wsdl']
            class_obj = vidyo_class(username, password, wsdl)
            if m.group(1):
                roomID = m.group(1).replace(':','')
            else:
                raise ResthttpckEx("RoomID is misssing, profile cant be changed.")
            profile = None
            if m.group(2):
                profile = m.group(2).replace(':','')

            getattr(class_obj, 'ToggleRoomProfile')(roomID=roomID,
                                                   profile=profile)
        m = re.match(r'GetRoomProfile(:\d+)', results.whichtest, re.IGNORECASE)
        if m:
            wsdl = APPCONFIG['vidyo']['admin_wsdl']
            class_obj = vidyo_class(username, password, wsdl)
            if m.group(1):
                roomID = m.group(1).replace(':', '')
            else:
                raise ResthttpckEx("RoomID is missing, profile cant be changed.")

            getattr(class_obj, 'GetRoomProfile')(roomID=roomID)

        m = re.match(r'UpdateRoomOwner(:\d+)(:\w+)?', results.whichtest, re.IGNORECASE)
        if m:
            wsdl = APPCONFIG['vidyo']['admin_wsdl']
            class_obj = vidyo_class(username, password, wsdl)
            if m.group(1):
                extension = m.group(1).replace(':', '')
            else:
                raise ResthttpckEx("Extension is required to find the room.")
            if m.group(2):
                owner = m.group(2).replace(':', '')
            else:
                raise ResthttpckEx("New owner of the room is missing.")

            getattr(class_obj, 'UpdateRoomOwner')(extension=extension, owner=owner)


        #else:
        #    wsdl = APPCONFIG['vidyo']['admin_wsdl']
        #    class_obj = vidyo_class(username, password, wsdl)
        #    getattr(class_obj, results.whichtest)()
    else:
        RestLogger.debug("Not matching class")

    # send the job


