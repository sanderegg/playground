build:
	docker compose build
	$(MAKE) -C sleeper build

build-devel:
	docker compose -f docker-compose.yml -f docker-compose.debug.yml build
	$(MAKE) -C sleeper build

up-standard:
	docker compose up
	# open http://127.0.0.1:8000/doc

# up:
# 	UID=$(shell id -u) GID=$(shell id -g) GID=$(shell getent group docker | cut -d: -f3) docker compose up

# up-devel:
# 	UID=$(shell id -u) GID=$(shell id -g) GID=$(shell getent group docker | cut -d: -f3) docker compose -f docker-compose.yml -f docker-compose.debug.yml up

# up-swarm:
# 	UID=$(shell id -u) GID=$(shell id -g) GID=$(shell getent group docker | cut -d: -f3) docker stack deploy -c docker-compose.yml user_stack

# up-swarm-devel:
# 	UID=$(shell id -u) GID=$(shell id -g) GID=$(shell getent group docker | cut -d: -f3) docker stack deploy -c docker-compose.yml -c docker-compose.debug.yml user_stack
down:
	-@docker-compose down
	-@docker stack rm user_stack

