from distributed import Client, SpecCluster, Worker, get_worker


def _retrieve_annotations() -> dict | None:
    import time

    worker = get_worker()
    task = worker.state.tasks.get(worker.get_current_task())
    print(f"retrieved {task=}")
    print(f"{task.annotations=}")
    print("going to sleep 1 seconds")
    time.sleep(1)
    return task.annotations


TASK_RESOURCES = {"RAM": 123}
WORKER_RESOURCES = {"CPU": 2.0, "RAM": 223423}

if __name__ == "__main__":
    cluster = SpecCluster(
        workers={
            "cpu-worker": {
                "cls": Worker,
                "options": {
                    # "nthreads": 2,
                    "resources": WORKER_RESOURCES,
                },
            }
        }
    )
    dask_client = Client(cluster)
    print(dask_client.dashboard_link)
    future = dask_client.submit(_retrieve_annotations, resources=TASK_RESOURCES)
    assert future
    dask_client.datasets["myfuture"] = future
    result = future.result()

    assert result == {"resources": TASK_RESOURCES}
