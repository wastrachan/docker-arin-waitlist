.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help message
	@echo ""
	@echo "Docker arin-waitlist Makefile"
	@echo "Usage: make [target]"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5); next } \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' \
		$(MAKEFILE_LIST)
	@echo ""

IMAGE=wastrachan/arin-waitlist
TAG=latest
REGISTRY=docker.io

.PHONY: build
build:	## Build and tag image
	@docker build -t ${REGISTRY}/${IMAGE}:${TAG} .

.PHONY: push
push:	## Push tagged image to registry
	@docker push ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: run
run: build	## Start container in the background with locally mounted volume
	docker run --name arin-waitlist \
			   --rm \
			   -e UPDATE_SCHEDULE="*/5 * * * *" \
			   -e SLACK_EMOJI=":timhortons:" \
			   -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/123" \
			   -e SLACK_TITLE="ARIN Waitlist" \
			   -e ARIN_WAITLIST_TIME="2024-02-02T19:58:22.198+00:00" \
	           ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: stop
stop:	## Stop running container
	@docker stop arin-waitlist

.PHONY: delete
delete:	## Delete all built image versions
	@docker image ls | grep ${IMAGE} | awk '{print $$3}' | xargs -I + docker rmi +
