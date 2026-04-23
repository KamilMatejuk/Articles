UID := $(shell id -u)
GID := $(shell id -g)

.PHONY: build run

build:
	docker compose build --build-arg UID=$(UID) --build-arg GID=$(GID)

run:
	docker compose up
