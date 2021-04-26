from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "IT'IS Foundation",
    "description": "the typical sidecar run",
    "start_date": days_ago(2),
}

with DAG("sidecar_dag", default_args=default_args) as dag:
    t1 = BashOperator(task_id="print_current_date", bash_command="date")

    t2 = DockerOperator(
        task_id="run_sidecar",
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

    t3 = BashOperator(task_id="print_hello", bash_command='echo "hello world"')

    t1 >> t2 >> t3
