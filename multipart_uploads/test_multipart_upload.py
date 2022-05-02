from typing import Callable
import boto3
from faker import Faker
import pytest
from moto import mock_s3


class MyModel(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(Bucket="mybucket", Key=self.name, Body=self.value)


from pathlib import Path

from pydantic import ByteSize, parse_obj_as

FILE_SIZE = parse_obj_as(ByteSize, "1 GiB")


@pytest.fixture
def create_files(tmp_path, faker):
    def _creator() -> Path:
        file_path: Path = tmp_path / faker.file_name()
        file_path.touch()
        file_path.write_text("x" * FILE_SIZE)
        assert file_path.exists()
        print("file size:", file_path.stat().st_size)
        return file_path

    return _creator


def test_multipart_upload(create_files, bucket: str, s3_client):
    another_local_file = create_files()
    s3_client.upload_file(
        Filename=f"{another_local_file}",
        Bucket=bucket,
        Key=another_local_file.name,
    )
    print("Existing objects:", s3_client.list_objects(Bucket=bucket))


import json


def test_create_federation_token(bucket: str, s3_client, faker: Faker):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": [f"arn:aws:s3:::{bucket}/<key-folder>/*"],
            }
        ],
    }
    sts = boto3.client("sts")
    list_of_credentials = []
    for n in range(1000):
        credentials = sts.get_federation_token(
            Name=faker.name(), Policy=json.dumps(policy), DurationSeconds=900
        )
        assert credentials
        list_of_credentials.append(credentials)
    print(f"-->created {len(list_of_credentials)}")
    # NOTE: with moto, it's always the same credentials... so that's not proper for testing


def test_access_real_bucket(real_s3_client, test_bucket: str):
    print(
        f"found following objects in bucket {real_s3_client.list_objects_v2(Bucket=test_bucket)}"
    )

@pytest.fixture
def real_sts_client(s3_settings):
    sts = boto3.client("sts", **s3_settings)
    assert sts
    yield sts


@pytest.fixture
def create_temporary_credentials_for_file(real_sts_client, test_bucket: str) -> Callable:
    def _creator(token_name: str, folder_name: str, duration_in_secs: int = 900):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": [f"arn:aws:s3:::{test_bucket}/testing_temporary_credentials/{folder_name}/*"],
                }
            ],
        }
        credentials = real_sts_client.get_federation_token(
            Name=token_name, Policy=json.dumps(policy), DurationSeconds=duration_in_secs
        )
        assert credentials
        return credentials
    return _creator


def test_create_temporary_credentials_in_real_bucket(real_s3_client, test_bucket: str):
