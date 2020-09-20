#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_glacier_db

:Synopsis:

:Author:
    servilla
  
:Created:
    1/15/17
"""
from datetime import datetime
from pathlib import Path

import daiquiri
import pytest
from sqlalchemy.exc import IntegrityError

from glacier_db import GlacierDb

logger = daiquiri.getLogger('test_glacier_db.py: ' + __name__)
DB = 'glacier_upload_log_test.sqlite'


@pytest.fixture()
def gdb():
    return GlacierDb(DB)


@pytest.fixture()
def cleanup():
    yield
    Path(DB).unlink(missing_ok=True)


def test_add_records(gdb, cleanup):
    gdb.add_upload_record(
        package='knb-lter-nin.1.1',
        identifier='2034saf0923',
        location='https://aws/glacier/2034saf0923',
        size=734563,
        checksum='AB9F90234E234D',
        timestamp=datetime.now())

    gdb.add_upload_record(
        package='knb-lter-nin.2.1',
        identifier='823lkas09234',
        location='https://aws/glacier/823lkas09234',
        size=89234,
        checksum='3243A12FD23',
        timestamp=datetime.now())


def test_record_collision(gdb, cleanup):
    gdb.add_upload_record(
        package='knb-lter-nin.1.1',
        identifier='2034saf0923',
        location='https://aws/glacier/2034saf0923',
        size=734563,
        checksum='AB9F90234E234D',
        timestamp=datetime.now())

    with pytest.raises(IntegrityError):
        gdb.add_upload_record(
            package='knb-lter-nin.1.1',
            identifier='2034saf0923',
            location='https://aws/glacier/2034saf0923',
            size='734563',
            checksum='AB9F90234E234D',
            timestamp=datetime.now()
        )


def test_package_exists(gdb, cleanup):
    gdb.add_upload_record(
        package='knb-lter-nin.1.1',
        identifier='2034saf0923',
        location='https://aws/glacier/2034saf0923',
        size=734563,
        checksum='AB9F90234E234D',
        timestamp=datetime.now())

    gdb.add_upload_record(
        package='knb-lter-nin.2.1',
        identifier='823lkas09234',
        location='https://aws/glacier/823lkas09234',
        size=89234,
        checksum='3243A12FD23',
        timestamp=datetime.now())

    gdb.add_upload_record(
        package='knb-lter-nin.3.1',
        identifier='ljd92ls2klj',
        location='https://aws/glacier/ljd92ls2klj',
        size=92348,
        checksum='345B03E223F',
        timestamp=datetime.now())

    # Test for existing package
    exists = gdb.package_exists(package='knb-lter-nin.3.1')
    assert exists

    # Test for non-existing package
    exists = gdb.package_exists(package='knb-lter-non.3.1')
    assert not exists
