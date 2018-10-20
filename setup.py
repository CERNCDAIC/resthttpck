#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

"""
resthttpck
"""

from setuptools import setup, find_packages

setup(name='resthttpck',
      version='0.1.0',
      description='A console app for testing rest services',
      author='CERN',
      author_email='rgaspar@cern.ch',
      license='GPLv3',
      maintainer='Ruben Gaspar',
      maintainer_email='rgaspar@cern.ch',
      url='https://github.com/cerncdaic/resthttpck',
      packages=find_packages(),
      scripts=[],
      test_suite="",
      install_requires=[
          'requests'
          ],
      )