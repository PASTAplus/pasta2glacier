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
import logging

import pasta2glacier

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('test_pasta2glacier')


class TestGetDataDirectories(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_directory_listing(self):
        data_path = '../data'
        dir_names = pasta2glacier.getDataDirectories(path=data_path)
        self.assertIsNotNone(dir_names)


if __name__ == '__main__':
    unittest.main()