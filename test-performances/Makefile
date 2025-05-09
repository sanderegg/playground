# Image and container names
IMAGE_NAME = aiohttp-server
CONTAINER_NAME = aiohttp-server-container

# Default port mapping (host:container)
PORT = 8080:8080

.PHONY: build run stop clean logs shell help

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container (detached mode)
run:
	docker run --name $(CONTAINER_NAME) -d -p $(PORT) $(IMAGE_NAME)

# Run the container (interactive mode)
run-it:
	docker run --name $(CONTAINER_NAME) -it -p $(PORT) $(IMAGE_NAME)

# Run with custom port
run-port:
	@read -p "Enter port (host:container, e.g. 9000:8080): " port; \
	docker run --name $(CONTAINER_NAME) -d -p $$port $(IMAGE_NAME)

# Stop and remove the container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Clean everything (stop container, remove container and image)
clean: stop
	docker rmi $(IMAGE_NAME) || true

# View container logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Open shell in running container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash || docker exec -it $(CONTAINER_NAME) /bin/sh

# Restart the container
restart: stop run

# Help command
help:
	@echo "Available commands:"
	@echo "  make build      - Build the Docker image"
	@echo "  make run        - Run the container in detached mode"
	@echo "  make run-it     - Run the container in interactive mode"
	@echo "  make run-port   - Run with custom port mapping"
	@echo "  make stop       - Stop and remove the container"
	@echo "  make clean      - Remove container and image"
	@echo "  make logs       - View container logs"
	@echo "  make shell      - Open a shell in the running container"
	@echo "  make restart    - Restart the container"

# Default target
.DEFAULT_GOAL := help
