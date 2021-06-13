## this is a test make file and is not to be used

SHELL := /bin/bash

include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV)
	activate

.PHONY: activate ## activate virtual environment
activate:
	eval source $(VENV)/bin/activate

.PHONY: install
install: ## Make venv and install requirements
	$(VENV)/bin/pip install wheel
	$(VENV)/bin/pip install -r requirements.txt

migrate: ## Make and run migrations
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

up: ## run docker compose and start the Docker container in the background
	docker-compose up -d

build: ## Access the Postgres Docker database interactively with psql
	docker-compose build

.PHONY: test
test: ## Run tests
	$(PYTHON) $(APP_DIR)/manage.py test application --verbosity=0 --parallel --failfast

.PHONY: run
run: ## Run the Django server
	$(PYTHON) $(APP_DIR)/manage.py runserver

start: install migrate run ## Install requirements, apply migrations, then start development server
