#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_lock

:Synopsis:

:Author:
    servilla
  
:Created:
    3/31/17
"""
from pathlib import Path
import re

import daiquiri

from lock import Lock


logger = daiquiri.getLogger('test_lock.py: ' + __name__)


def test_lock_construction_no_name():
    lock_file = re.compile(r'(\D){10}.lock')
    lock = Lock()
    fn = lock.lock_file
    match = lock_file.match(fn)
    assert(match is not None)


def test_lock_construction_with_name():
    lock = Lock('bozo.lock')
    fn = lock.lock_file
    assert(fn == 'bozo.lock')


def test_lock_acquire_release():
    lock = Lock()
    fn = lock.lock_file
    lock.acquire()
    lock_exists = Path(fn).exists()
    assert lock_exists
    lock.release()
    lock_exists = Path(fn).exists()
    assert not lock_exists
    Path(fn).unlink(missing_ok=True)
