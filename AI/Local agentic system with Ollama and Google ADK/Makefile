PROJECT_NAME=local_agentic_system

build:
	docker compose -p $(PROJECT_NAME) build

up:
	docker compose -p $(PROJECT_NAME) up -d && \
	docker compose -p $(PROJECT_NAME) logs -f

down:
	docker compose -p $(PROJECT_NAME) down -v
