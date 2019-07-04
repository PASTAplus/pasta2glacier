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

from datetime import datetime
import logging
import os
import shutil
import sys

from boto3.exceptions import Boto3Error
import click
import daiquiri

from glacier_db import GlacierDb
from glacier import Glacier
from lock import Lock

log_file = 'p2g.log'
daiquiri.setup(level=logging.INFO,
               outputs=(
                   'stderr',
                   daiquiri.output.File(filename=f'{log_file}')
                ))
logger = daiquiri.getLogger('pasta2glacier.py: ' + __name__)


def data_directories(path=None):
    if path and os.path.isdir(path):
        return os.listdir(path)
    else:
        err_msg = 'Path "{path}" is not a directory.'.format(path=path)
        raise IOError(err_msg)


def ignores(ignore_file: str) -> list:
    pids = list()
    if ignore_file is not None:
        with open(ignore_file, 'r') as f:
            pids = [_.strip() for _ in f.readlines()]
    return pids


def mock_response():
    r = {
        'archiveId': '2bf5l58c52IXU67qovKRk49Np5vYACZELD4rhWOL86kIi3-ncU-WM-v7hG8l9TuTiT12xmiloa67WsMUGdrxOKVejKdFYA5F7Ksmdlifq_gARt6a7rwR5oFDl5jyH3ACjGh8P83eBg',
        'location': '/321492031925/vaults/PASTA_Test/archives/2bf5l58c52IXU67qovKRk49Np5vYACZELD4rhWOL86kIi3-ncU-WM-v7hG8l9TuTiT12xmiloa67WsMUGdrxOKVejKdFYA5F7Ksmdlifq_gARt6a7rwR5oFDl5jyH3ACjGh8P83eBg',
        'checksum': '226cb0468dcda728f80bd5807e6483cbbb191b5f9e7cb0b61fd51c11acb30d01'}
    return r


help_dryrun = 'Dry run only - no AWS Glacier upload'
help_noclean = 'Do not remove tarballs after archiving'
help_force = 'Force creation of archives even if they already exist'
help_limit = 'Limit upload to \'n\' archives'
help_ignore = 'File containing package identifiers to ignore one per line'
help_work = 'Working directory path'
help_lock = 'Location of lock file'

@click.command()
@click.argument('vault')
@click.argument('data_path')
@click.option('-d', '--dryrun', default=False, is_flag=True, help=help_dryrun)
@click.option('-n', '--noclean', default=False, is_flag=True, help=help_noclean)
@click.option('-f',  '--force', default=False, is_flag=True, help=help_force)
@click.option('--limit', default=None, type=int, help=help_limit)
@click.option('--ignore', default=None, type=str, help=help_ignore)
@click.option('--workdir', default='/tmp', type=str, help=help_work)
@click.option('--lockfile', default='/tmp/glacier.lock', type=str, help=help_lock)
def main(vault: str, data_path: str, dryrun: bool, noclean: bool, force: bool,
         limit: int, ignore: str, workdir: str, lockfile: str):
    """
    pasta2glacier provides a mechanism to upload archived (zip or tar) data
    packages from the PASTA data repository into Amazon's AWS Glacier storage.

    \b
    vault       The AWS Glacier vault to be used (e.g. "PASTA_Test")
    data_path   The file system path to the local data directory
    """

    multipart_threshold = (1024**2) * (2**10)  # 1GB
    part_size = (1024**2) * (2**10)  # 1GB

    lock = Lock(lockfile)
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

    try:
        ignore_pids = ignores(ignore)
        os.chdir(workdir)
        for dir_name in data_directories(data_path):

            logger.debug('Directory {cnt} of {dirs}: {dir_name}'.format(cnt=cnt,
                         dirs=dirs, dir_name=dir_name))
            cnt += 1

            if not gdb.package_exists(dir_name) and dir_name not in ignore_pids:

                if limit is not None:
                    if limit > 0:
                        limit -= 1
                    else:
                        break

                archive = f'{dir_name}.tar.gz'
                if os.path.exists(archive) and not force:
                    msg = f'Archive file {archive} exists, will use instead of creating new archive'
                    logger.info(msg)
                else:
                    logger.info(f'Create archive: {archive}')
                    archive = shutil.make_archive(base_name=dir_name,
                                                  format='gztar',
                                                  base_dir=dir_name,
                                                  root_dir=data_path,
                                                  dry_run=dryrun)
                archive_size = os.path.getsize(archive)
                archive_description = f'{dir_name}'

                if not dryrun:
                    try:
                        glacier = Glacier(vault_name=vault)
                        if archive_size < multipart_threshold:
                            response = glacier.do_upload(archive=archive,
                                    archive_description=archive_description)
                        else:
                            response = glacier.do_multipart_upload(archive=archive,
                                        archive_description=archive_description,
                                        part_size=part_size)
                        logger.info('Response: {response}'.format(response=response))
                        gdb.add_upload_record(package=dir_name,
                                              identifier=response['archiveId'],
                                              location=response['location'],
                                              size=archive_size,
                                              checksum=response['checksum'],
                                              timestamp=datetime.now())
                    except Exception as e:
                        logger.error(e)
                    finally:
                        if not noclean:
                            os.remove(archive)

            else:
                logger.debug('Skipping directory {}'.format(dir_name))
    except Exception as e:
        logger.ERROR(e)
    finally:
        lock.release()
        logger.info('Lock file {} released'.format(lock.lock_file))
    return 0


if __name__ == "__main__":
    main()
