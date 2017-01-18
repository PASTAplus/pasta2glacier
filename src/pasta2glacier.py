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
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('pasta2glacier')

from glacier_db import GlacierDb
from glacier import Glacier


def getDataDirectories(path=None):
    if path and os.path.isdir(path):
        directories = os.listdir(path)
    return directories


def main():

    data_path = '../data'
    archive_path = '../archive'

    gdb = GlacierDb()
    gdb.connect_glacier_upload_log_db()


    for dir_name in getDataDirectories(data_path):
        if not gdb.package_exists(dir_name):
            archive = shutil.make_archive(base_name=archive_path + '/' +
                                                    dir_name,
                                          format='gztar', base_dir=dir_name,
                                          root_dir=data_path)

            archive_description = 'This archive ({dir_name}) is a data ' \
                                  'package derived from the PASTA ecological ' \
                                  'and environmental data repository. Unless ' \
                                  'stated otherwise, all contents of this ' \
                                  'data package are licensed under Creative ' \
                                  'Commons CC-0.'.format(dir_name=dir_name)

            g = Glacier(vault_name='PASTA_Test')
            response = g.do_multipart_upload(archive=archive,
                                        archive_description=archive_description)
            print(response)
            # TODO: register upload in glacier_db
            os.remove(archive)

    return 0


if __name__ == "__main__":
    main()