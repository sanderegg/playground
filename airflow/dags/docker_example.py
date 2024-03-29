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
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
}

dag = DAG(
    "docker_sample",
    default_args=default_args,
    start_date=days_ago(2),
)

t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

t3 = DockerOperator(
    api_version="auto",
    command="echo 'hello from inside the container!!!'",
    force_pull=True,
    image="ubuntu:latest",
    task_id="docker_op_tester",
    network_mode="bridge",
    dag=dag,
)


t4 = BashOperator(task_id="print_hello", bash_command='echo "hello world!!!"', dag=dag)


t1 >> t2
t1 >> t3
t3 >> t4