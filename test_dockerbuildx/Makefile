BUILD_REGISTRY_URL:=127.0.0.1:15000
LOCAL_REGISTRY_URL:=127.0.0.1:5000

build-registry:
	$(MAKE) --no-print-directory --directory /home/sanderegg/dev/github/osparc-simcore .docker-build-registry

local-registry:
	$(MAKE) --no-print-directory --directory /home/sanderegg/dev/github/osparc-simcore local-registry

build-without-push: build-registry
	docker buildx build \
	--cache-from type=registry,ref=$(BUILD_REGISTRY_URL)/image \
	--cache-to type=registry,ref=$(BUILD_REGISTRY_URL)/image,mode=max \
	.

build-with-cache: build-registry local-registry
	docker buildx build \
	--cache-from type=registry,ref=$(BUILD_REGISTRY_URL)/cache \
	--cache-to type=registry,ref=$(BUILD_REGISTRY_URL)/cache,mode=max \
	--tag $(LOCAL_REGISTRY_URL)/image:latest \
	--push .

build-with-bake-no-push: build-registry local-registry
	export LOCAL_REGISTRY=$(LOCAL_REGISTRY_URL); \
	docker buildx bake \
		--set first_service.cache-from=type=registry,ref=$(BUILD_REGISTRY_URL)/first_service:cache \
		--set first_service.cache-to=type=registry,ref=$(BUILD_REGISTRY_URL)/first_service:cache,mode=max \
		--set second_service.cache-from=type=registry,ref=$(BUILD_REGISTRY_URL)/second_service:cache \
		--set second_service.cache-to=type=registry,ref=$(BUILD_REGISTRY_URL)/second_service:cache,mode=max \
		--file docker-compose.yml

build-with-bake: build-registry local-registry
	export LOCAL_REGISTRY=$(LOCAL_REGISTRY_URL); \
	docker buildx bake \
		--set first_service.cache-from=type=registry,ref=$(BUILD_REGISTRY_URL)/first_service:cache \
		--set first_service.cache-to=type=registry,ref=$(BUILD_REGISTRY_URL)/first_service:cache,mode=max \
		--set second_service.cache-from=type=registry,ref=$(BUILD_REGISTRY_URL)/second_service:cache \
		--set second_service.cache-to=type=registry,ref=$(BUILD_REGISTRY_URL)/second_service:cache,mode=max \
		--set *.output=type=registry,push=true \
		--file docker-compose.yml

list-build-registry-contents:
	@curl --silent -X GET $(BUILD_REGISTRY_URL)/v2/_catalog | jq .repositories
	@curl --silent -X GET $(BUILD_REGISTRY_URL)/v2/first_service/tags/list | jq
	@curl --silent -H "Accept: application/vnd.docker.distribution.manifest.v2+json"  \
			-X GET $(BUILD_REGISTRY_URL)/v2/first_service/manifests/cache

list-local-registry-contents:
	@curl --silent -X GET $(LOCAL_REGISTRY_URL)/v2/_catalog | jq
	@curl --silent -X GET $(LOCAL_REGISTRY_URL)/v2/image/tags/list | jq
	@curl --silent -H "Accept: application/vnd.docker.distribution.manifest.v2+json"  -X GET $(LOCAL_REGISTRY_URL)/v2/image/manifests/latest | jq

clean:
	# cleaning...
	-@docker buildx prune --force
	-@docker rm -f registry
	-@docker rm -f build_registry
	-@docker volume rm registry
	# ... done