.PHONY: test

ENV=PYTHONPATH=. CONN_STR=postgresql://postgres:postgres@localhost:5432/trias RMQ_HOST=localhost

# Auxillary tasks

install:
	pipenv install

lint:
	pipenv run isort -y && pipenv run flake8

up:
	docker-compose up -d

down:
	docker-compose down

# Development tasks

frontend:
	pipenv run gunicorn trias.frontend.app:app

backend:
	${ENV} pipenv run python -c 'from trias.backend.worker import work; work()'

test:
	${ENV} pipenv run pytest -v

term:
	${ENV} pipenv run python

# Admin tasks

db_init:
	${ENV} pipenv run python -c 'import trias.database.admin as db; db.create_tables(); db.load_samples()'

take_room:
	${ENV} pipenv run python -c 'import trias.backend.admin as be; be.take_room()'
