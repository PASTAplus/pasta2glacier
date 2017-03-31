#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: lock

:Synopsis:
    Create a simple file-based mutex lock.
 
:Author:
    servilla

:Created:
    3/31/17
"""

import logging
import string
import random
import os

logger = logging.getLogger('lock')


class Lock(object):

    def __init__(self, file_name=None):

        if file_name is None:
            self._file_name = '/tmp/glacier.lock'
        else:
            self._file_name = file_name

    def acquire(self):
        fp = open(self._file_name, 'wb')
        fp.close()

    def release(self):
        os.remove(self._file_name)

    @property
    def locked(self):
        return os.path.isfile(self._file_name)

    @property
    def lock_file(self):
        return self._file_name


def main():
    return 0


if __name__ == "__main__":
    main()