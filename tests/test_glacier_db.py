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
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('test_glacier_db')

from glacier_db import GlacierDb


class TestDatabase(unittest.TestCase):

    def setUp(self):
        db_name = 'glacier_upload_log_test.sqlite'
        self.gdb = GlacierDb(db_name)
        self.gdb.connect_glacier_upload_log_db()


    def tearDown(self):
        self.gdb.delete_glacier_upload_log_db()
        pass

    def test_add_records(self):
        self.gdb.add_upload_record(
            package='knb-lter-nin.1.1',
            identifer='2034saf0923',
            location='https://aws/glacier/2034saf0923',
            size='734563',
            checksum='AB9F90234E234D',
            timestamp=datetime.now())

        self.gdb.add_upload_record(
            package='knb-lter-nin.2.1',
            identifer='823lkas09234',
            location='https://aws/glacier/823lkas09234',
            size='89234',
            checksum='3243A12FD23',
            timestamp=datetime.now())


    def test_record_collision(self):
        self.gdb.add_upload_record(
            package='knb-lter-nin.1.1',
            identifer='2034saf0923',
            location='https://aws/glacier/2034saf0923',
            size='734563',
            checksum='AB9F90234E234D',
            timestamp=datetime.now())

        self.assertRaises(IntegrityError,
                          self.gdb.add_upload_record,
                          package='knb-lter-nin.1.1',
                          identifer='2034saf0923',
                          location='https://aws/glacier/2034saf0923',
                          size='734563',
                          checksum='AB9F90234E234D',
                          timestamp=datetime.now())


    def test_package_exists(self):
        self.gdb.add_upload_record(
            package='knb-lter-nin.1.1',
            identifer='2034saf0923',
            location='https://aws/glacier/2034saf0923',
            size='734563',
            checksum='AB9F90234E234D',
            timestamp=datetime.now())

        self.gdb.add_upload_record(
            package='knb-lter-nin.2.1',
            identifer='823lkas09234',
            location='https://aws/glacier/823lkas09234',
            size='89234',
            checksum='3243A12FD23',
            timestamp=datetime.now())

        self.gdb.add_upload_record(
            package='knb-lter-nin.3.1',
            identifer='ljd92ls2klj',
            location='https://aws/glacier/ljd92ls2klj',
            size='92348',
            checksum='345B03E223F',
            timestamp=datetime.now())

        # Test for existing package
        exists = self.gdb.package_exists(package='knb-lter-nin.3.1')
        self.assertTrue(exists)

        # Test for non-existing package
        exists = self.gdb.package_exists(package='knb-lter-non.3.1')
        self.assertFalse(exists)


if __name__ == '__main__':
    unittest.main()