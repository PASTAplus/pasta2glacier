#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_glacier_db

:Synopsis:

:Author:
    servilla
  
:Created:
    1/15/17
"""

import unittest
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('test_glacier_db')


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()