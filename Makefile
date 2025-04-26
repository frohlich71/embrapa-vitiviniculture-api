ENV_FILE=.env
PYTHON=python
MODULE=app.cli.ingest

run:
	PYTHONPATH=. fastapi dev app/main.py

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
	$(PYTHON) -m $(MODULE) commercialization

ingest-importation:
	$(PYTHON) -m $(MODULE) importation

init:
	make migrate
	make ingest-production
	make ingest-processing
	make ingest-commercialization
	make ingest-importation
# Instalação de dependências
install:
	pip install -r requirements.txt
