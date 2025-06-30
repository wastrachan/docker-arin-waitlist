.PHONY: help
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "Docker arin-waitlist image makefile"
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
	docker run --name arin-waitlist \
			   --rm \
			   -e UPDATE_SCHEDULE="*/5 * * * *" \
			   -e SLACK_EMOJI=":timhortons:" \
			   -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/123" \
			   -e SLACK_TITLE="ARIN Waitlist" \
			   -e ARIN_WAITLIST_TIME="2024-02-02T19:58:22.198+00:00" \
	           ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: stop
stop:
	@docker stop arin-waitlist

.PHONY: delete
delete:
	@docker image ls | grep ${IMAGE} | awk '{print $$3}' | xargs -I + docker rmi +
