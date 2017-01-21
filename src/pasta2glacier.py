#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta2glacier

:Synopsis:
    To add PASTA data packages to the Amazon AWS Glacier storage.

:Author:
    servilla
  
:Created:
    1/15/17
"""
import os
import shutil
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z', filename='../p2g.log',
                    level=logging.INFO)
logger = logging.getLogger('pasta2glacier')

from glacier_db import GlacierDb
from glacier import Glacier


def getDataDirectories(path=None):

    if path and os.path.isdir(path):
        return os.listdir(path)
    else:
        err_msg = 'Path "{path}" is not a directory.'.format(path=path)
        raise IOError(err_msg)

def main():

    data_path = '../data'
    archive_path = '../archive'
    multipart_threshold = (1024 ** 2) * 4  # 4MB

    gdb = GlacierDb('glacier_upload_log.sqlite')
    gdb.connect_glacier_upload_log_db()


    for dir_name in getDataDirectories(data_path):
        logger.info('Directory: {dir_name}'.format(dir_name=dir_name))
        if not gdb.package_exists(dir_name):
            archive = shutil.make_archive(base_name=archive_path + '/' +
                                                    dir_name,
                                          format='gztar', base_dir=dir_name,
                                          root_dir=data_path)
            logger.info('Create archive: {archive}'.format(archive=archive))
            archive_size = os.path.getsize(archive)

            archive_description = 'This archive ({dir_name}) is a data ' \
                                  'package derived from the PASTA ecological ' \
                                  'and environmental data repository. Unless ' \
                                  'stated otherwise, all contents of this ' \
                                  'data package are licensed under Creative ' \
                                  'Commons CC-0.'.format(dir_name=dir_name)

            glacier = Glacier(vault_name='PASTA_Test')

            if (archive_size < multipart_threshold):
                response = glacier.do_upload(archive=archive,
                                        archive_description=archive_description)
            else:
                response = glacier.do_multipart_upload(archive=archive,
                                        archive_description=archive_description)

            logger.info('Response: {response}'.format(response=response))

            gdb.add_upload_record(package=dir_name,
                                  identifier=response['archiveId'],
                                  location=response['location'],
                                  size=archive_size,
                                  checksum=response['checksum'],
                                  timestamp=datetime.now())

            os.remove(archive)

    return 0


if __name__ == "__main__":
    main()