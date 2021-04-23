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

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from pprint import pformat
def extract_dag_run_arguments(**kwargs):
    print("received pipeline arguments", pformat(kwargs["dag_run"].conf))
    return kwargs["dag_run"].conf

with DAG(
    "templated_dag", default_args=default_args, schedule_interval=None, catchup=False
) as dag:
    start_task = DummyOperator(task_id="start")
    extract_pipeline_task = PythonOperator(
            task_id="python_task",
            python_callable=extract_dag_run_arguments,
            provide_context=True
        )
    end_task = DummyOperator(task_id="end")

    TEST_VALUE = 4
    log.info("the current test value is %s", TEST_VALUE)
    for index in range(TEST_VALUE):
        dynamic_task: DockerOperator = create_comp_task(task_id=f"comp_task_{index}")

        start_task >> dynamic_task
        dynamic_task >> end_task




    # start_task >> extract_pipeline_task >> end_task
