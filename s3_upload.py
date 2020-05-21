import boto3
import os
import logging
import common.credentials as cred
from boto3.s3.transfer import S3Transfer

aws_access_key_id = cred.aws_access_key_id  #
aws_secret_access_key = cred.aws_access_key  #

bucket_name = "fetsim-logs"
bucket_folder = "fetsim-logs"
log_file_extension = ".log"


def upload():
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    for subdir, dirs, files in os.walk("logs"):
        for file in files:
            if file.endswith(log_file_extension):
                logging.info("Upload: {}".format(file))
                fetsim_origin_file = os.path.join(subdir, file)
                bucket_dest_file = bucket_folder + "/" + file
                transfer = S3Transfer(client)
                transfer.upload_file(
                    filename=fetsim_origin_file,
                    bucket=bucket_name,
                    key=bucket_dest_file,
                )
