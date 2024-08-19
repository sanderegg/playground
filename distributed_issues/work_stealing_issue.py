import asyncio
import datetime
import math
from pprint import pprint
import dask.config
from distributed import Client, Scheduler, SpecCluster, Worker, get_worker
import distributed


async def _sleeper(time_to_sleep: datetime.timedelta) -> int:
    total_sleep_time = 0
    while slept := await asyncio.sleep(1, result=True):
        total_sleep_time += slept
        print(f"{total_sleep_time=}/{time_to_sleep.total_seconds()}")
        if total_sleep_time >= time_to_sleep.total_seconds():
            break
    print(f"we are done sleeping {total_sleep_time} seconds!")
    return total_sleep_time


TASK_RESOURCES = {"RAM": 123}
WORKER_RESOURCES = {"CPU": 2.0, "RAM": 223423}
TIME_TO_SLEEP = datetime.timedelta(seconds=300)


async def _start_task(
    dask_client: distributed.Client, task_name: str, time_to_sleep: datetime.timedelta
) -> distributed.Future:
    future = dask_client.submit(
        _sleeper, time_to_sleep, resources=TASK_RESOURCES, pure=False
    )
    assert future
    await dask_client.publish_dataset(future, name=task_name)
    return future


async def _start_tasks(
    dask_client: distributed.Client, num_tasks: int, time_to_sleep: datetime.timedelta
) -> list[distributed.Future]:
    futures = await asyncio.gather(
        *(
            _start_task(
                dask_client,
                task_name=f"myfuture-{n}-{datetime.datetime.now(datetime.timezone.utc)}",
                time_to_sleep=time_to_sleep,
            )
            for n in range(num_tasks)
        )
    )
    print(f"{num_tasks} tasks passed to scheduler")
    return futures


async def _scale_cluster(
    cluster: distributed.SpecCluster, desired_num_workers: int, delay_s: int
) -> None:
    while len(cluster.workers) != desired_num_workers:
        increment = math.copysign(1, desired_num_workers - len(cluster.workers))
        new_workers_number = len(cluster.workers) + increment
        print(f"scaling cluster to {new_workers_number}")
        await cluster.scale(new_workers_number)
        await asyncio.sleep(delay_s)

    print(f"scaled cluster to {desired_num_workers} workers")


async def _join_futures(futures: list[distributed.Future]) -> None:
    await asyncio.gather(*(f.result() for f in futures))


async def main():
    scheduler_spec = {"cls": Scheduler, "options": {"dashboard_address": ":8787"}}
    worker_spec = {
        "cls": Worker,
        "options": {"nthreads": 1, "resources": WORKER_RESOURCES},
    }
    # with dask.config.set({"distributed.scheduler.worker-saturation": 1.0}):
    async with SpecCluster(
        scheduler=scheduler_spec,
        worker=worker_spec,
        asynchronous=True,
    ) as cluster:
        pprint(dask.config.config)
        # no workers
        cluster.scale(0)

        async with Client(cluster, asynchronous=True) as dask_client:
            # start 8x sleepers at 300s
            print(dask_client.dashboard_link)
            initial_num_tasks = 8
            initial_time_to_sleep = datetime.timedelta(seconds=300)
            futures = await _start_tasks(
                dask_client, initial_num_tasks, initial_time_to_sleep
            )
            # wait a bit
            await asyncio.sleep(15)
            await _scale_cluster(cluster, desired_num_workers=8, delay_s=5)
            await asyncio.sleep(15)

            # second wave
            second_wave_num_tasks = 6
            second_wave_time_to_sleep = datetime.timedelta(seconds=60)
            second_wave_futures = await _start_tasks(
                dask_client, second_wave_num_tasks, second_wave_time_to_sleep
            )
            # scale up cluster
            await asyncio.sleep(5)
            await _scale_cluster(cluster, desired_num_workers=10, delay_s=5)
            await asyncio.sleep(10)

            await _join_futures(futures + second_wave_futures)

            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
