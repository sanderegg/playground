import s3fs
fs = s3fs.S3FileSystem(anon=False, key="12345678", secret="12345678", client_kwargs={"endpoint_url": "http://127.0.0.1:9001"})
files = fs.ls('simcore')
print("following files found:", f"{files}")