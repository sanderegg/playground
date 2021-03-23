import json

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}
@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['docker'])
def sidecar():

    @task()
    def first_task():
        print("Hello from the first task")

    task_one = first_task()


    # docker_task = DockerOperator(api_version='1.19',
    # docker_url='tcp://localhost:2375',  # Set your docker URL
    # command='/bin/sleep 30',
    # image='centos:latest',
    # network_mode='bridge',
    # task_id='docker_op_tester',
    # dag=dag,)

    # task_one >> docker_task

sidecar_dag = sidecar()