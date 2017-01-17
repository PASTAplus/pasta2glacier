#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: glacier

:Synopsis:

:Author:
    servilla
  
:Created:
    1/16/17
"""

import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('glacier')

import boto3


class Glacier(object):

    def __init__(self):
        self.glacier = boto3.resource('glacier')

    def get_vaults(self):
        return self.glacier.vaults.all()

    def do_multipart_upload(self, archive_path=None):

        pass
        # try:
        #     initiate_multipart_upload()
        #     iterate over archive for byte size
        #         upload_multipart_part()
        #     complete_multipart_upload()
        # except:
        #     abort_multipart_upload()
        #     raise MultipartUploadError()


class MultipartUploadError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


def main():

    g = Glacier()
    for vault in g.get_vaults():
        print('{}'.format(vault.name))

    return 0


if __name__ == "__main__":
    main()