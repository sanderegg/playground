export PUBLIC_NETWORK=public
export MONITORED_NETWORK=monitored
export TRAEFIK_SIMCORE_ZONE=the_zone
export SWARM_STACK_NAME=simcore
export TRAEFIK_USER=admin
export TRAEFIK_PASSWORD=$(shell docker run --rm --entrypoint htpasswd registry:2.6 -nb user password | sed -e s/\\$$/\\$$\\$$/g)
export MONITORING_DOMAIN=monitoring.osparc.local
export PUBLISHED_HOST_NAME=osparc.local


up:
	docker stack deploy -c docker-compose.yml ops

down:
	docker stack rm ops

up-simcore:
	docker stack deploy -c docker-compose-simcore.yml simcore

down-simcore:
	docker stack rm simcore

up-aws:
	docker stack deploy -c docker-compose-simcore-aws.yml simcore
down-aws:
	docker stack rm simcore
