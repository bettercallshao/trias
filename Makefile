.PHONY: test

install:
	pipenv install

dev:
	pipenv run gunicorn trias:frontend

test:
	CONN_STR=postgresql://postgres:postgres@localhost:5432/trias \
	PYTHONPATH=. \
	pipenv run pytest -v

lint:
	pipenv run isort -y && pipenv run flake8

up:
	docker-compose up -d

down:
	docker-compose down

# admin tasks

initdb:
	CONN_STR=postgresql://postgres:postgres@localhost:5432/trias \
	pipenv run python -c 'import trias.admin; trias.admin.init_db()'

takeroom:
	CONN_STR=postgresql://postgres:postgres@localhost:5432/trias \
	pipenv run python -c 'import trias.admin; trias.admin.take_room()'
