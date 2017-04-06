#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta2glacier

:Synopsis:
    The main workflow loop to archive PASTA data packages to the Amazon AWS
    Glacier data storage.

:Author:
    servilla
  
:Created:
    1/15/17
"""

import os
import shutil
from datetime import datetime
import logging
import sys

from boto3.exceptions import Boto3Error
from docopt import docopt

from glacier_db import GlacierDb
from glacier import Glacier

from lock import Lock

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='p2g.log',
                    level=logging.INFO)

logger = logging.getLogger('pasta2glacier')


def data_directories(path=None):
    if path and os.path.isdir(path):
        return os.listdir(path)
    else:
        err_msg = 'Path "{path}" is not a directory.'.format(path=path)
        raise IOError(err_msg)


def mock_response():
    r = {}
    r[
        'archiveId'] = '2bf5l58c52IXU67qovKRk49Np5vYACZELD4rhWOL86kIi3-ncU-WM-v7hG8l9TuTiT12xmiloa67WsMUGdrxOKVejKdFYA5F7Ksmdlifq_gARt6a7rwR5oFDl5jyH3ACjGh8P83eBg'
    r[
        'location'] = '/321492031925/vaults/PASTA_Test/archives/2bf5l58c52IXU67qovKRk49Np5vYACZELD4rhWOL86kIi3-ncU-WM-v7hG8l9TuTiT12xmiloa67WsMUGdrxOKVejKdFYA5F7Ksmdlifq_gARt6a7rwR5oFDl5jyH3ACjGh8P83eBg'
    r[
        'checksum'] = '226cb0468dcda728f80bd5807e6483cbbb191b5f9e7cb0b61fd51c11acb30d01'
    return r


def main(argv):
    """
    pasta2glacier provides a mechanism to upload archived (zip or tar) data
    packages from the PASTA data repository into Amazon's AWS Glacier storage.

    Usage:
        pasta2glacier.py <vault> <data_path> [-d | --dry] [-l | --limit <n>]
        pasta2glacier.py (-h | --help)
        
    Arguments:
        vault       The AWS Glacier vault to be used (e.g. "PASTA_Test")
        data_path   The file system path to the local data directory

    Options:
        -h --help         This page
        -d --dry          Dry run only - no AWS Glacier upload
        -l --limit <n>    Limit upload to 'n' archives
        
    """

    args = docopt(str(main.__doc__))
    DRY_RUN = args['--dry']
    vault = args['<vault>']
    data_path = args['<data_path>']

    if len(args['--limit']) == 1:
        limit = int(args['--limit'][0])
    else:
        limit = None

    multipart_threshold = (1024 ** 2) * 99  #99MB
    part_size = (1024**2) * (2**5)

    lock = Lock('/tmp/glacier.lock')
    if lock.locked:
        logger.error('Lock file {} exists, exiting...'.format(lock.lock_file))
        return 1
    else:
        lock.acquire()
        logger.info('Lock file {} acquired'.format(lock.lock_file))

    gdb = GlacierDb('glacier_upload_log.sqlite')
    gdb.connect_glacier_upload_log_db()

    dirs = len(data_directories(data_path))
    cnt = 1
    for dir_name in data_directories(data_path):

        logger.info('Directory {cnt} of {dirs}: {dir_name}'.format(cnt=cnt,
                     dirs=dirs, dir_name=dir_name))
        cnt += 1
        if not gdb.package_exists(dir_name):

            if limit is not None:
                if limit > 0:
                    limit -= 1
                else:
                    break

            archive = shutil.make_archive(base_name=dir_name, format='gztar',
                                          base_dir=dir_name, root_dir=data_path)
            logger.info('Create archive: {archive}'.format(archive=archive))
            archive_size = os.path.getsize(archive)

            archive_description = '{dir_name}'.format(dir_name=dir_name)

            if DRY_RUN:
                response = mock_response()
            else:
                try:

                    glacier = Glacier(vault_name=vault)

                    if (archive_size < multipart_threshold):
                        response = glacier.do_upload(archive=archive,
                                        archive_description=archive_description)
                    else:
                        response = glacier.do_multipart_upload(archive=archive,
                                        archive_description=archive_description,
                                                  part_size=part_size)

                except Boto3Error as e:
                    logger.error(e)
                    return -1

            logger.info('Response: {response}'.format(response=response))

            gdb.add_upload_record(package=dir_name,
                                  identifier=response['archiveId'],
                                  location=response['location'],
                                  size=archive_size,
                                  checksum=response['checksum'],
                                  timestamp=datetime.now())
            os.remove(archive)

        else:
            logger.info('Skipping directory {}'.format(dir_name))

    lock.release()
    logger.info('Lock file {} released'.format(lock.lock_file))
    return 0


if __name__ == "__main__":
    main(sys.argv)
