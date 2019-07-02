#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_pasta2glacier

:Synopsis:

:Author:
    servilla
  
:Created:
    1/15/17
"""
import unittest

import daiquiri

import pasta2glacier

logger = daiquiri.getLogger('test_pasta2glacier.py: ' + __name__)


class TestGetDataDirectories(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_directory_listing(self):
        data_path = '../data'
        dir_names = pasta2glacier.data_directories(path=data_path)
        self.assertIsNotNone(dir_names)


if __name__ == '__main__':
    unittest.main()