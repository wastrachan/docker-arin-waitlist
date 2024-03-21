# ARIN Waitlist Docker Image

.PHONY: help
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "Docker ARIN waitlist image makefile"
	@echo ""
	@echo "Commands:"
	@echo "  build        Build and tag image"
	@echo "  push         Push tagged image to registry"
	@echo "  run          Start container in the background with locally mounted volume"
	@echo "  stop         Stop and remove container running in the background"
	@echo "  delete       Delete all built image versions"
	@echo ""

IMAGE=wastrachan/arin-waitlist
TAG=latest
REGISTRY=docker.io

.PHONY: build
build:
	@docker build -t ${REGISTRY}/${IMAGE}:${TAG} .

.PHONY: push
push:
	@docker push ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: run
run: build
	@docker run --name arin-waitlist \
               --rm \
               -e ARIN_WAITLIST_TIME="Tue, 25 Feb 2020 13:07:29" \
               -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/TTtttttTT" \
               -d \
               ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: stop
stop:
	@docker stop arin-waitlist

.PHONY: delete
delete:
	@docker image ls | grep ${IMAGE} | awk '{print $$3}' | xargs -I + docker rmi +
