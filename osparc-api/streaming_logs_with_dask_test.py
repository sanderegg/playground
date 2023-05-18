import dask
import dask.distributed
import subprocess
import time

# create a Dask cluster
# cluster = dask.distributed.LocalCluster()

# create a Dask client
client = dask.distributed.Client()

# define a function to stream the logs of a container and yield them as they are generated
def stream_container_logs(container_name):
    command = f"docker run --name {container_name} hello-world"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

    # wait for the process to finish and get the return code
    process.wait()
    rc = process.returncode

    # raise an exception if the process exited with a non-zero return code
    if rc != 0:
        raise Exception(f"Container exited with return code {rc}")

# start streaming the logs of the container on one of the Dask workers
future = client.submit(stream_container_logs, "my_container")

# loop through the log lines as they are generated
for line in future.result():
    print(line.decode("utf-8").strip())
