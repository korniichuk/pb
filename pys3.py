# -*- coding: utf-8 -*-
# Name: pys3
# Version: 0.1a2
# Owner: Ruslan Korniichuk

import boto3


def upload_file(s3_bucket, src, dst, logger=None):
    """Upload file to Amazon S3 bucket.

     Args:
        s3_bucket -- name of Amazon S3 bucket (required | type: string),
        src -- path to local source file (required | type: string),
        dst -- Amazon S3 bucket dst file abs path (required | type: string),
        logger -- loguru logger (not required | type: loguru._logger.Logger).
    """

    try:
        s3 = boto3.resource('s3')
        s3.Bucket(s3_bucket).upload_file(src, dst)
    except BaseException as e:
        if logger:
            logger.error(e)
        return 1
    else:
        if logger:
            text = "'{}' file was uploaded to '{}' Amazon S3 bucket as '{}'"
            msg = text.format(src, s3_bucket, dst)
            logger.info(msg)
