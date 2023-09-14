from dask.distributed import Client, LocalCluster
from dask.distributed import Security


def inc(x):
    return x + 1


def add(x, y):
    return x + y


def run_test():
    security = Security(
        tls_ca_file="dask.crt",
        tls_client_cert="dask.crt",
        tls_client_key="dask.key",
        tls_scheduler_cert="dask.crt",
        tls_scheduler_key="dask.key",
        tls_worker_cert="dask.crt",
        tls_worker_key="dask.key",
        require_encryption=True,
    )
    security = Security.temporary()

    # cluster = LocalCluster(
    #     security=security
    # )  # Launches a scheduler and workers locally
    # client = Client(
    #     cluster, security=security
    # )  # Connect to distributed cluster and override default
    client = Client("tls://192.168.1.20:8000")
    a = client.submit(inc, 1)  # work starts immediately
    b = client.submit(inc, 2)  # work starts immediately
    c = client.submit(add, a, b)  # work starts immediately

    c = c.result()  # block until work finishes, then gather result
    print(c)


if __name__ == "__main__":
    run_test()


# NOTES:
# openssl req -newkey rsa:4096 -nodes -sha256 -x509 -days 3650 -nodes -subj "/C=CH/L=Zurich/CN=osparc.io" -out myca.pem -keyout mykey.pem
#
#
# perplexity
# openssl genrsa -out dask.key 2048
# openssl req -new -x509 -key dask.key -out dask.crt -days 3650
