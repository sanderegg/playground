from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "description": "run the sleepers",
    "start_date": days_ago(2),
}

with DAG("sleepers_dag", default_args=default_args) as dag:
    t1 = BashOperator(task_id="print_current_date", bash_command="date")

    t2 = DockerOperator(
        task_id="run_sleeper",
        image="itisfoundation/sleeper:1.0.0",
        api_version="auto",
        force_pull=True,
        auto_remove=False,
        command="run",
        network_mode="bridge",
        volumes=[
            "airflow_inputs:/input",
            "airflow_outputs:/output",
            "airflow_logs:/log",
        ],
        environment={
            "INPUT_FOLDER": "/input",
            "OUTPUT_FOLDER": "/output",
            "LOG_FOLDER": "/log",
        },
    )

    t3 = BashOperator(task_id="print_hello", bash_command='echo "hello world"')

    t1 >> t2 >> t3
