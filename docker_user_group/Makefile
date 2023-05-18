up:
	UID=$(id -u) GID=$(id -g) DOCKER_GROUP=$(getent group docker | cut -d: -f3) docker compose up

up-devel:
	UID=$(id -u) GID=$(id -g) DOCKER_GROUP=$(getent group docker | cut -d: -f3) docker compose -f docker-compose.yml -f docker-compose.debug.yml up

down:
	docker-compose down