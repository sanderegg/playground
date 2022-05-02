from typing import Iterator
from moto import mock_s3, mock_sts
from faker import Faker
import boto3
import pytest
import botocore


@pytest.fixture
def s3_client():
    with mock_s3(), mock_sts():
        s3 = boto3.client("s3", region_name="us-east-1")
        yield s3


from typing import Any


@pytest.fixture
def s3_settings() -> dict[str, Any]:
    return {
        "aws_access_key_id": "AKIATHZO54NSPQJIWRU3",
        "aws_secret_access_key": "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",
        "region_name": "us-east-1",
    }


@pytest.fixture
def real_s3_client(s3_settings):
    s3 = boto3.client("s3", **s3_settings)
    print(f"found following buckets: {s3.list_buckets().get('Buckets')}")
    yield s3


@pytest.fixture
def test_bucket() -> str:
    return "staging-simcore"


@pytest.fixture
def bucket(faker: Faker, s3_client) -> Iterator[str]:
    BUCKET_NAME = "my_bucket"
    s3_client.create_bucket(Bucket=BUCKET_NAME)
    print("-->buckets in S3:", s3_client.list_buckets())

    yield BUCKET_NAME
    objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    print(
        f"<-- emptying bucket {BUCKET_NAME} of {objects=}",
    )
    if "Contents" in objects:
        s3_client.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={"Objects": [{"Key": obj["Key"]} for obj in objects["Contents"]]},
        )
    s3_client.delete_bucket(Bucket=BUCKET_NAME)
    print("<--buckets in S3 after removal:", s3_client.list_buckets())
