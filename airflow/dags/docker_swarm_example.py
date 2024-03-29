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
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker_swarm import DockerSwarmOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    "docker_swarm_sample",
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    start_date=days_ago(1),
    catchup=False,
)

with dag as dag:
    t1 = DockerSwarmOperator(
        api_version="auto",
        command="echo 'hello from inside the the service!!!'",
        image="ubuntu:latest",
        auto_remove=True,
        task_id="sleep_with_swarm",
        enable_logging=False,  # airflow bug: https://github.com/apache/airflow/issues/13675
    )