.PHONY: test

install:
	pipenv install

dev:
	pipenv run gunicorn trias:app

test:
	pipenv run pytest

lint:
	pipenv run isort -y && pipenv run flake8

up:
	docker-compose up -d

down:
	docker-compose down
