#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_pasta2glacier

:Synopsis:

:Author:
    servilla
  
:Created:
    1/15/17
"""
import daiquiri
import pytest

import pasta2glacier

logger = daiquiri.getLogger('test_pasta2glacier.py: ' + __name__)


def test_directory_listing():
    data_path = '../data'
    dir_names = pasta2glacier.data_directories(path=data_path)
    assert dir_names is not None
