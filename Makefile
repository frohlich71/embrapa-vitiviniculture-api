# Variáveis
ENV_FILE=.env
PYTHON=python
MODULE=app.cli.ingest

# Comandos de desenvolvimento
run:
	PYTHONPATH=. fastapi dev app/main.py

test:
	pytest --cov=app tests/

lint:
	ruff check .

format:
	ruff format .

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "auto migration"

ingest-production:
	$(PYTHON) -m $(MODULE) --source=production

# Instalação de dependências
install:
	pip install -r requirements.txt
