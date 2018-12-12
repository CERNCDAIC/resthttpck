#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.


import configparser
import sys
import traceback

import os
from base.RestLogger import RestLogger


CONFIG = None
APPCONFIG = {}

FILELOGS = '/etc/resthttpck/logging.conf'
FILEINI = '/etc/resthttpck/resthttpck.ini'
FILESTEMP = '/var/log/resthttpck/files'

RestLogger(name='resthttpck', logconfig='/etc/resthttpck/logging.conf')
RestLogger.debug("logger has been initialised")

try:
    # Load configuration from file
    CONFIG = configparser.ConfigParser()
    CONFIG.read(FILEINI)


    if CONFIG.has_section('sorenson'):
        APPCONFIG['sorenson'] = {}
        if CONFIG.has_option('sorenson', 'url'):
            APPCONFIG['sorenson']['url'] = CONFIG.get('sorenson', 'url')
        if CONFIG.has_option('sorenson', 'presetids'):
            APPCONFIG['sorenson']['presetids'] = CONFIG.get('sorenson', 'presetids').split(',')
        if CONFIG.has_option('sorenson', 'queueid'):
            APPCONFIG['sorenson']['queueid'] = CONFIG.get('sorenson', 'queueId').split(',')
        if CONFIG.has_option('sorenson', 'username01'):
            APPCONFIG['sorenson']['username01'] = CONFIG.get('sorenson', 'username01')
        if CONFIG.has_option('sorenson', 'password01'):
            APPCONFIG['sorenson']['password01'] = CONFIG.get('sorenson', 'password01')
        if CONFIG.has_option('sorenson', 'masterfiles'):
            APPCONFIG['sorenson']['masterfiles'] = CONFIG.get('sorenson', 'masterfiles').split(',')
        if CONFIG.has_option('sorenson', 'masterfiles_path'):
            APPCONFIG['sorenson']['masterfiles_path'] = CONFIG.get('sorenson', 'masterfiles_path')
        # Build all possible master files
        APPCONFIG['sorenson']['fileurimaster'] = []
        for f in APPCONFIG['sorenson']['masterfiles']:
            APPCONFIG['sorenson']['fileurimaster'].append(os.path.join(APPCONFIG['sorenson']['masterfiles_path'], f))

        if CONFIG.has_option('sorenson', 'fileuritest'):
            APPCONFIG['sorenson']['fileuritest'] = CONFIG.get('sorenson', 'fileuritest')
        if CONFIG.has_option('sorenson', 'fileuritestwild'):
            APPCONFIG['sorenson']['fileuritestwild'] = CONFIG.get('sorenson', 'fileuritestwild')
        #if CONFIG.has_option('sorenson', 'createjob_tpl'):
        #    APPCONFIG['sorenson']['createjob_tpl'] = CONFIG.get('sorenson', 'createjob_tpl')
        # db related
        if CONFIG.has_option('sorenson', 'mysql_host'):
            APPCONFIG['sorenson']['mysql_host'] = CONFIG.get('sorenson', 'mysql_host')
        if CONFIG.has_option('sorenson', 'mysql_port'):
            APPCONFIG['sorenson']['mysql_port'] = CONFIG.get('sorenson', 'mysql_port')
        if CONFIG.has_option('sorenson', 'mysql_user'):
            APPCONFIG['sorenson']['mysql_user'] = CONFIG.get('sorenson', 'mysql_user')
        if CONFIG.has_option('sorenson', 'mysql_db'):
            APPCONFIG['sorenson']['mysql_db'] = CONFIG.get('sorenson', 'mysql_db')
        if CONFIG.has_option('sorenson', 'mysql_password'):
            APPCONFIG['sorenson']['mysql_password'] = CONFIG.get('sorenson', 'mysql_password')
        if CONFIG.has_option('sorenson', 'mysql_chartset'):
            APPCONFIG['sorenson']['mysql_charset'] = CONFIG.get('sorenson', 'mysql_charset')

        # check if all important values are present, exit in negative case
        important_names_sorenson = ['url', 'presetids', 'queueid', 'username01', 'password01']
        if not all(name in APPCONFIG['sorenson'] for name in important_names_sorenson):
            print('Some important options are missing, please check your ini file')
            sys.exit(1)
    if CONFIG.has_section('general'):
        APPCONFIG['general'] = {}
        APPCONFIG['general']['tempfiles'] = CONFIG.get('general', 'tempfiles')
        APPCONFIG['general']['jobidfiles'] = CONFIG.get('general', 'jobidfiles')
    if CONFIG.has_section('vidyo'):
        APPCONFIG['vidyo'] = {}
        APPCONFIG['vidyo']['username'] = CONFIG.get('vidyo', 'username')
        APPCONFIG['vidyo']['password'] = CONFIG.get('vidyo', 'password')
        APPCONFIG['vidyo']['admin_wsdl'] = CONFIG.get('vidyo', 'admin_wsdl')
        APPCONFIG['vidyo']['owner'] = CONFIG.get('vidyo', 'owner')
        APPCONFIG['vidyo']['mysql_db'] = CONFIG.get('vidyo', 'mysql_db')
        APPCONFIG['vidyo']['sqlpath'] = CONFIG.get('vidyo', 'sqlpath')
        APPCONFIG['vidyo']['sqllogs'] = CONFIG.get('vidyo', 'sqllogs')

except IOError as e:
    traceback.print_exc(file=sys.stdout)
    sys.exit(e.code)
except configparser.NoOptionError:
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
