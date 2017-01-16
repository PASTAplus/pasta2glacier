#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: glacier_db

:Synopsis:

:Author:
    servilla
  
:Created:
    1/15/17
"""

import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('glacier_db')

from sqlalchemy import Column, Integer, Float, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class GlacierUploadLog(Base):

    __tablename__ = 'glacier_upload_log'

    package = Column(String, primary_key=True)
    identifier = Column(String, nullable=False)
    location = Column(String, nullable=False)
    size = Column(String, nullable=False)
    checksum = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


def connect_glacier_upload_log_db():
    os.chdir('../db')
    cwd = os.getcwd()
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///' + cwd + '/glacier_upload_log.sqlite')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()


def add_upload_record(package=None, identiifer=None, location=None, size=None,
                      checksum=None, timestamp=None, session=None):

    record = GlacierUploadLog(
        package = package,
        identifier = identiifer,
        location = location,
        size = size,
        checksum = checksum,
        timestamp = timestamp)

    session.add(record)
    session.commit()


def main():
    return 0



if __name__ == "__main__":
    main()