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

Base = declarative_base()


class GlacierUploadLog(Base):

    __tablename__ = 'glacier_upload_log'

    package = Column(String, primary_key=True)
    identifier = Column(String, nullable=False)
    location = Column(String, nullable=False)
    size = Column(String, nullable=False)
    checksum = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class GlacierDb(object):

    def __init__(self, db_name='glacier_upload_log.sqlite'):
        os.chdir('../db')
        cwd = os.getcwd()
        self.db_path = cwd + '/' + db_name

    def connect_glacier_upload_log_db(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///' + self.db_path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def delete_glacier_upload_log_db(self):
        os.remove(self.db_path)

    def add_upload_record(self, package=None, identifer=None, location=None,
                          size=None, checksum=None, timestamp=None):

        record = GlacierUploadLog(
            package = package,
            identifier = identifer,
            location = location,
            size = size,
            checksum = checksum,
            timestamp = timestamp)

        self.session.add(record)
        self.session.commit()

    def package_exists(self, package=None):
        record = self.session.query(GlacierUploadLog).filter(
            GlacierUploadLog.package == package).one_or_none()
        if record:
            return True
        else:
            return False


def main():
    return 0



if __name__ == "__main__":
    main()