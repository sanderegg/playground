import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

# import networkx as nx
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago


log = logging.getLogger(__file__)

default_args = {
    "owner": "airflow",
    "description": "run the sleepers",
    "start_date": days_ago(2),
}



# def create_computational_pipeline(computational_dag: nx.DiGraph):
    # for node in nx.topological_sort(computational_dag):
        


def create_comp_task(task_id: str) -> DockerOperator:
    return DockerOperator(
        task_id=task_id,
        image="itisfoundation/sidecar:master-github-latest",
        api_version="auto",
        force_pull=True,
        auto_remove=False,
        command="simcore-service-sidecar --help",
        network_mode="bridge",
        volumes=[
            "airflow_inputs:/home/scu/input",
            "airflow_outputs:/home/scu/output",
            "airflow_logs:/home/scu/log",
            "/var/run/docker.sock:/var/run/docker.sock",
            "/etc/hostname:/home/scu/hostname:ro",
        ],
        environment={},
    )

with DAG("templated_dag", default_args=default_args) as dag:
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    TEST_VALUE = 4
    log.info("the current test value is %s", TEST_VALUE)
    for index in range(TEST_VALUE):
        dynamic_task: DockerOperator = create_comp_task(task_id=f"comp_task_{index}")

        start_task >> dynamic_task
        dynamic_task >> end_task


    start_task >> end_task
