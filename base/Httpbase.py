#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import requests
from ResthttpckEx import ResthttpckEx
from requests.auth import HTTPBasicAuth
from base.RestLogger import RestLogger

class Httpbase:

    @staticmethod
    def GetREST(url, headers, authpair):
        #url = "https://webhook.site/b2cd0c09-fb09-4b7a-a3be-ea9d6a8a8e8c/api/jobs/status/b1b0f16c-bdba-493f-bda8-3a39b4a8d9f3/"
        resp = requests.get(url, verify=False, headers=headers, auth=HTTPBasicAuth(authpair[0], authpair[1]))
        if not requests.codes.ok == resp.status_code:
            # This means something went wrong.
            raise ResthttpckEx('GET {} {} {}'.format(url, resp.status_code, resp.text), resp.status_code)
        return resp
        #for todo_item in resp.json():
        #    print('{} {}'.format(todo_item['id'], todo_item['summary']))

    @staticmethod
    def PostREST(url, data_json, files,  headers, authpair):
        resp = None
        if files:
            resp = requests.post(url,  headers=headers, files=files,
                                 verify=False, auth=HTTPBasicAuth(authpair[0], authpair[1]))
        else:
            resp = requests.post(url, headers=headers, json=data_json,
                                 verify=False, auth=HTTPBasicAuth(authpair[0], authpair[1]))
        if not requests.codes.ok == resp.status_code:
            raise ResthttpckEx('POST url: {} return_code: {} body: {}'.format(url, resp.status_code, resp.text),
                               resp.status_code)
        RestLogger.debug('Created task headers: {} return code: {} text: {} json: {}'.format(resp.headers,
                                                                                          resp.status_code,
                                                                                          resp.text,
                                                                                          resp.json))
        return resp