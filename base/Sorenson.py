#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import json
import os
import re

from ResthttpckEx import ResthttpckEx
from base.Utils import Utils
from base.RestLogger import RestLogger
from base.Httpbase import Httpbase

from config import APPCONFIG

class Sorenson:

    def __init__(self, single=False, title=None):
        self.single = single
        self.title = title

    def transcoding_job(self, title='A default job', single=False):
        self.title = title
        self.single = single
        return self._CreateJobs(title, single)

    def query_job(self, timing, status_job):
        arr = Utils.FilesYoungerthan(APPCONFIG['general']['jobidfiles'], int(timing))
        for f in arr:
            try:
                response=self.GetSorenson(f)
                RestLogger.debug('Job status: {}'.format(json.dumps(json.loads(response.text),
                                                                    indent=2,
                                                                    sort_keys=True)))

            except ResthttpckEx as ex:
                if ex.http_error_code == 404:
                    RestLogger.debug('jobid {} likely over, removing from filesystem'.format(f))
                    os.remove(os.path.join(APPCONFIG['general']['jobidfiles'], f))

    def GetSorenson(self, jobid):
        username = re.sub(r'CERN\\{1,}', "", APPCONFIG['sorenson']['username01'])
        RestLogger.debug('Sending request on behalf {}'.format(username))
        response = Httpbase.GetREST(url="{}status/{}/".format(APPCONFIG['sorenson']['url'], jobid),
                                    headers={'Accept': 'application/json'},
                                    authpair=(username, APPCONFIG['sorenson']['password01']))
        return response
    def _CreateJobs(self, title, single=False):
        pathtotpl = os.path.join('../templates', 'sorenson_transcoding_job.txt')
        if not os.path.exists(pathtotpl):
            raise ResthttpckEx('No createjob template found')

        return self._CreateJobFromtpl(pathtotpl)


    def _FormatGeneralFieldtpl(self, field):
        '''


        :param field: it's a tuple e.g. ('username','value')
        :return:
        '''

        fieldclean = field.replace('#','')
        if fieldclean == 'title':
            RestLogger.debug("title is {}".format(self.title))
            return (field, '"{}"'.format(self.title))
        if fieldclean in APPCONFIG['sorenson'].keys():
            RestLogger.debug(fieldclean)
            if fieldclean == 'presetids':
                if not self.single:
                    RestLogger.debug(APPCONFIG['sorenson']['presetids'])
                    pids = ['{' + '"PresetId": "{}"'.format(n) + '}' for n in APPCONFIG['sorenson']['presetids']]
                    joinpids = ','.join(pids)
                    RestLogger.debug("{}".format(joinpids))
                    return (field, "{}".format(joinpids))
                else:
                    RestLogger.debug('PresetId is {}'.format(Utils.GivemeOne(APPCONFIG['sorenson']['presetids'])))
                    return (field, '{' + '"PresetId": "{}"'.format(Utils.GivemeOne(APPCONFIG['sorenson']['presetids'])) + '}')
            if isinstance(APPCONFIG['sorenson'][fieldclean], list):
                RestLogger.debug('"{}"'.format(Utils.GivemeOne(APPCONFIG['sorenson'][fieldclean])))
                return (field, '"{}"'.format(Utils.GivemeOne(APPCONFIG['sorenson'][fieldclean])))
            else:
                RestLogger.debug('{} "{}"'.format(fieldclean, APPCONFIG['sorenson'][fieldclean]))
                return (field, '"{}"'.format(APPCONFIG['sorenson'][fieldclean]))

    def _CreateJobFromtpl(self, pathtotpl):
        '''We are trying to build a json like:
        {
            "QueueId": "4ec0f503-2256-4a05-873f-1747da859e7c",
            "JobMediaInfo": {"CompressionPresetList": [{"PresetId": "15322a69-c0e3-4333-95b7-86d6dceb0e53"},{"PresetId": "e87ae9f2-ceab-412e-a5e7-5c180f156762"}, {"PresetId": "ed4133a6-dfcb-407e-89d2-5a74d23961bb"}, {"PresetId": "9d301467-3f22-41ea-add5-9bf829be6e1c"}],
            "SourceMediaList": [{"UserName": "CERN\\XXXXX", "Password": "XXXXXXX", "FileUri": "file://cern.ch/dfs/Scratch/webcast/portrait/CERN-FOOTAGE-2005-03.avi"}],
            "DestinationList": [{"FileNamingMethod":"Wildcard","FileUri": "file://cern.ch/dfs/Scratch/webcast/portrait/result/%SOURCE%_%JOBID%_%PRESET%"}]},
            "Name": "Portrait case"
        }'''
        RestLogger.debug(pathtotpl)
        tpl = Utils.ReadFile(pathtotpl)
        valuestoreplace = Utils.FindAll(r'#\w*#', tpl)

        finalstr = tpl
        RestLogger.debug(finalstr)
        for v in valuestoreplace:
            finalstr = Utils.ReplaceStr(v, finalstr, self._FormatGeneralFieldtpl(v)[1])
            RestLogger.debug(finalstr)
        myname = Utils.GenerateName('sorenson')
        with open(os.path.join(APPCONFIG['general']['tempfiles'], myname), 'w') as newfile:
            newfile.write(finalstr)

        # Return file to job
        return os.path.join(APPCONFIG['general']['tempfiles'], myname)

    def PostSorenson(self, filetoberead):
        data_json = None
        username = re.sub(r'CERN\\{1,}', "", APPCONFIG['sorenson']['username01'])
        RestLogger.debug('Sending request on behalf {}'.format(username))
        with open(filetoberead) as jdata:
            data_json = json.load(jdata)
        response = Httpbase.PostREST(url=APPCONFIG['sorenson']['url'],
                                    data_json=data_json, files=None,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json'},
                                    authpair=(username, APPCONFIG['sorenson']['password01']))

        # print("response json {}".format(response.json()))
        # print("type {}".format(type(response.json())))
        # print(response.json()['JobId'])
        return response.json()




