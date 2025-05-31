ENV_FILE=.env
COMPOSE=docker-compose
SERVICE=web

# Docker Compose Management
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) down
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

logs:
	$(COMPOSE) logs -f

logs-web:
	$(COMPOSE) logs -f $(SERVICE)

logs-db:
	$(COMPOSE) logs -f db

# Development Commands (run inside Docker containers)
run:
	$(COMPOSE) up -d

test:
	$(COMPOSE) exec $(SERVICE) pytest --cov=app tests/

format:
	$(COMPOSE) exec $(SERVICE) black app tests

migrate:
	$(COMPOSE) exec $(SERVICE) alembic upgrade head

makemigrations:
	$(COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "auto migration"

# Data Ingestion Commands
ingest-production:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest run production

ingest-processing:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest run processing

ingest-commercialization:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest run commercialization

ingest-importation:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest run importation

ingest-exportation:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest run exportation

# Database Management
create-admin:
	$(COMPOSE) exec $(SERVICE) python -m app.cli.ingest init-admin

reset-db:
	$(COMPOSE) down
	$(COMPOSE) volume rm embrapa-vitiviniculture-api_postgres_data || true
	$(COMPOSE) up -d

# Full Setup Commands
init:
	$(COMPOSE) up -d
	sleep 10
	make migrate
	make create-admin
	make ingest-production
	make ingest-processing
	make ingest-commercialization
	make ingest-importation
	make ingest-exportation

init-all: build init

# Shell Access
shell:
	$(COMPOSE) exec $(SERVICE) bash

shell-db:
	$(COMPOSE) exec db psql -U postgres -d embrapa_vitiviniculture

# Status Commands
status:
	$(COMPOSE) ps

health:
	curl -f http://localhost:8000/ || echo "API not responding"

# Clean Commands
clean:
	$(COMPOSE) down -v
	docker system prune -f

install:
	@echo "Dependencies are installed during Docker build process"
	@echo "To rebuild with new dependencies, run: make rebuild"
