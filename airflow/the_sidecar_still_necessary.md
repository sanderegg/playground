# current workflow with sidecar

## init

1. Sidecar starts
2. Sidecar connects to Celery

## runtime

1. Sidecar receives a message from Celery containing **user_id, project_id, node_id**
2. Sidecar connects to RabbitMQ (logs,progress) and to Postgres (getting task information, service key, service version) -> ENVS: RABBIT, POSTGRES
3. Sidecar downloads inputs (values, link to files) -> ENVS: POSTGRES, STORAGE
4. Sidecar starts the service key:version, gets its logs, monitor the service -> REQS: DOCKER
5. Sidecar sends logs/progress over RabbitMQ -> ENVS: RABBIT
6. Sidecar waits for the service to stop or kills it
7. Sidecar gets the outputs and uploads them to Postgre/S3



# how could airflow be deployed?

## architecture

1. airflow scheduler
2. airflow webserver (optional)
3. database (postgres)
4. worker (celery or dask) (optional if DockerSwarmOperator is used instead of DockerOperator)
5. worker dependencies (rabbitMQ for celery, ...)


## airflow requirements

1. scheduler and worker(s) must have access to the same DAG files -> need of a shared file server (NFS server, S3)
2. the DAG file must be available beforehand -> a dynamic configuration can be passed to airflow when the DAG is started


## airflow limitations

1. DAG file configuration is kind of a hack
2. annoying shared server
3. no auto-scaling of resources

## workflow

1. director-v2 