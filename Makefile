.PHONY: test

install:
	pipenv install

initdb:
	CONN_STR=postgres://postgres:postgres@localhost:5432/trias \
	pipenv run python -c 'import trias.admin; trias.admin.init_db()'

dev:
	pipenv run gunicorn trias:frontend

test:
	pipenv run pytest

lint:
	pipenv run isort -y && pipenv run flake8

up:
	docker-compose up -d

down:
	docker-compose down
