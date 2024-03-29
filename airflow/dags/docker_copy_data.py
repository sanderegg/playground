#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=missing-function-docstring
"""
This sample "listen to directory". move the new file and print it,
using docker-containers.
The following operators are being used: DockerOperator,
BashOperator & ShortCircuitOperator.
TODO: Review the workflow, change it accordingly to
      your environment & enable the code.
"""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "docker_sample_copy_data",
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    start_date=days_ago(2),
)

locate_file_cmd = """
    sleep 10
    find {{params.source_location}} -type f  -printf "%f\n" | head -1
"""

t_view = BashOperator(
    task_id="view_file",
    bash_command=locate_file_cmd,
    do_xcom_push=True,
    params={"source_location": "/your/input_dir/path"},
    dag=dag,
)


def is_data_available(*args, **kwargs):
    """Return True if data exists in XCom table for view_file task, false otherwise."""
    ti = kwargs["ti"]
    data = ti.xcom_pull(key=None, task_ids="view_file")
    return not data == ""


t_is_data_available = ShortCircuitOperator(
    task_id="check_if_data_available", python_callable=is_data_available, dag=dag
)

t_move = DockerOperator(
    api_version="1.19",
    docker_url="tcp://localhost:2375",  # replace it with swarm/docker endpoint
    image="centos:latest",
    network_mode="bridge",
    volumes=[
        "/your/host/input_dir/path:/your/input_dir/path",
        "/your/host/output_dir/path:/your/output_dir/path",
    ],
    command=[
        "/bin/bash",
        "-c",
        "/bin/sleep 30; "
        "/bin/mv {{params.source_location}}/{{ ti.xcom_pull('view_file') }} {{params.target_location}};"
        "/bin/echo '{{params.target_location}}/{{ ti.xcom_pull('view_file') }}';",
    ],
    task_id="move_data",
    do_xcom_push=True,
    params={
        "source_location": "/your/input_dir/path",
        "target_location": "/your/output_dir/path",
    },
    dag=dag,
)

print_templated_cmd = """
    cat {{ ti.xcom_pull('move_data') }}
"""

t_print = DockerOperator(
    api_version="auto",
    docker_url="tcp://localhost:2375",
    image="centos:latest",
    volumes=["/your/host/output_dir/path:/your/output_dir/path"],
    command=print_templated_cmd,
    task_id="print",
    dag=dag,
)

t_view.set_downstream(t_is_data_available)
t_is_data_available.set_downstream(t_move)
t_move.set_downstream(t_print)