.PHONY: run migrate makemigrations test lint format shell superuser freeze setup

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

freeze:
	pip freeze > requirements.txt

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp -n .env.example .env || true
	python manage.py migrate
	@echo "✅ Setup complete!"
