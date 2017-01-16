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
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('test_glacier_db')

import glacier_db

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.session = glacier_db.connect_glacier_upload_log_db(
            'glacier_upload_log_test.sqlite')


    def tearDown(self):
        pass


    def test_add_record(self):
        glacier_db.add_upload_record(
            package='knb-lter-nin.1.1',
            identiifer='2034saf0923',
            location='https://aws/glacier/2034saf0923',
            size='734563',
            checksum='AB9F90234E234D',
            timestamp=datetime.now(),
            session=self.session)


if __name__ == '__main__':
    unittest.main()