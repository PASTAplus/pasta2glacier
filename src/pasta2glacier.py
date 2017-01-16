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
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('pasta2glacier')


def getDataDirectories(path=None):

    if path and os.path.isdir(path):
        directories = os.listdir(path)

    return directories


def main():
    return 0


if __name__ == "__main__":
    main()