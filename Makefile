ENV_FILE=.env
PYTHON=python
MODULE=app.cli.ingest

run:
	PYTHONPATH=. fastapi dev app/main.py

run-prod:
	PYTHONPATH=. python app/main.py

test:
	pytest --cov=app tests/


format:
	black app tests

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "auto migration"

ingest-production:
	$(PYTHON) -m $(MODULE) production

ingest-processing:
	$(PYTHON) -m $(MODULE) processing

ingest-commercialization:
	$(PYTHON) -m $(module) commercialization

init:
	make migrate
	make ingest-production
	make ingest-processing
	make ingest-commercialization
	make run-prod

# Instalação de dependências
install:
	pip install -r requirements.txt
