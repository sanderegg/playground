from typing import AsyncIterator, Callable, Coroutine
from distributed import Client, Scheduler, SpecCluster, Worker, get_worker
import pytest


@pytest.fixture
async def dask_spec_local_cluster(
    unused_tcp_port_factory: Callable,
) -> AsyncIterator[SpecCluster]:
    # in this mode we can precisely create a specific cluster
    workers = {
        "cpu-worker": {
            "cls": Worker,
            "options": {
                "nthreads": 2,
                "resources": {"CPU": 2, "RAM": 48e9},
            },
        },
        "gpu-worker": {
            "cls": Worker,
            "options": {
                "nthreads": 1,
                "resources": {
                    "CPU": 1,
                    "GPU": 1,
                    "RAM": 48e9,
                },
            },
        },
        "bigcpu-worker": {
            "cls": Worker,
            "options": {
                "nthreads": 1,
                "resources": {
                    "CPU": 8,
                    "RAM": 768e9,
                },
            },
        },
    }
    scheduler = {
        "cls": Scheduler,
        "options": {
            "port": unused_tcp_port_factory(),
            "dashboard_address": f":{unused_tcp_port_factory()}",
        },
    }

    async with SpecCluster(
        workers=workers, scheduler=scheduler, asynchronous=True, name="pytest_cluster"
    ) as cluster:
        yield cluster


@pytest.fixture
async def dask_client(dask_spec_local_cluster: SpecCluster) -> AsyncIterator[Client]:
    async with Client(
        dask_spec_local_cluster.scheduler_address, asynchronous=True, set_as_default=True
    ) as client:
        client.as_current()
        yield client
        client.as_current()


def _retrieve_annotations() -> None:
    worker = get_worker()
    task = worker.state.tasks.get(worker.get_current_task())
    return task.annotations


RESOURCES = {"CPU": 1.0, "RAM": 123423}


async def test_submit_future_with_resources(dask_client: Client):
    future = dask_client.submit(_retrieve_annotations, resources=RESOURCES)
    assert future
    coro = future.result()
    assert isinstance(coro, Coroutine)
    assert await coro == {"resources": RESOURCES}


# async def test_submit_future_with_resources_and_published_dataset(dask_client: Client):
#     future = dask_client.submit(_retrieve_annotations, resources=RESOURCES)
#     assert future
#     await dask_client.publish_dataset(future, name="myfuture")
#     coro = future.result()
#     assert isinstance(coro, Coroutine)
#     assert await coro == {"resources": RESOURCES}
