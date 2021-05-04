stack_name = airflow


.stack.airflow.yml: airflow-stack.yaml .env
	docker-compose --env-file .env --file $< --log-level=ERROR config > $@

up: .stack.airflow.yml
	docker stack deploy --compose-file $< $(stack_name)

down:
	docker stack rm $(stack_name)