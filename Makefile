# ARIN Waitlist Monitor Makefile
#
# Copyright (c) Winston Astrachan 2020
#
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "ARIN Waitlist Monitor Makefile"
	@echo ""
	@echo "Commands:"
	@echo "  build        Build and tag image"
	@echo "  clean        Mark image for rebuild"
	@echo "  delete       Delete image and mark for rebuild"
	@echo ""

build: .arin-waitlist.img

.arin-waitlist.img:
	docker build -t wastrachan/arin-waitlist:latest .
	@touch $@

.PHONY: clean
clean:
	rm -f .arin-waitlist.img

.PHONY: delete
delete: clean
	docker rmi -f wastrachan/arin-waitlist
