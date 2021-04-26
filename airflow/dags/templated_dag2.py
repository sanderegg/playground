import logging
from typing import Any, Dict, List

# import networkx as nx
from airflow import DAG
from airflow.models import Variable
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


import json
import os
from pprint import pformat

from airflow.operators.python import PythonOperator
from airflow import configuration as conf
from airflow.models import DagBag, TaskInstance
from airflow import DAG, settings


main_dag_id = "oSparc_DAG"


def extract_dag_run_arguments(**kwargs):
    pipeline_configuration = kwargs["dag_run"].conf
    print("received pipeline arguments", pformat(pipeline_configuration))
    log.info("setting airflow variables with workbench configuration")
    Variable.set(
        "Workbench",
        pipeline_configuration["value"],
    )
    log.info(
        "current airflow variable state is: %s",
        Variable.get("Workbench", default_var=None),
    )


from uuid import uuid4

with DAG(
    main_dag_id, default_args=default_args, schedule_interval=None, catchup=False
) as dag:
    start_task = DummyOperator(task_id="start")
    extract_comp_pipeline_from_conf_task = PythonOperator(
        task_id="extract_dagrun_arguments",
        python_callable=extract_dag_run_arguments,
        provide_context=True,
    )
    start_task >> extract_comp_pipeline_from_conf_task
    end_task = DummyOperator(task_id="end")

    dynamic_workflow_config = int(Variable.get("Workbench", default_var=0))
    log.info("TEST: the current configuration value is [%s]", dynamic_workflow_config)
    for index in range(dynamic_workflow_config):

        dynamic_task: DockerOperator = create_comp_task(
            task_id=f"comp_task.{index}_{uuid4()}"
        )

        extract_comp_pipeline_from_conf_task >> dynamic_task
        dynamic_task >> end_task
