import aioboto3

from moto import mock_s3


@mock_s3
async def test_aioboto3():
    session = aioboto3.Session()
    async with session.resource("s3") as s3:
        bucket = await s3.Bucket("mybucket")  # <----------------
        async for s3_object in bucket.objects.all():
            print(s3_object)
