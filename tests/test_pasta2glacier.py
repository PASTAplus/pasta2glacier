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

from config import Config
import pasta2glacier

logger = daiquiri.getLogger('test_pasta2glacier.py: ' + __name__)


def test_directory_listing():
    dir_names = pasta2glacier.data_directories(path=Config.DATA_PATH)
    assert dir_names is not None
