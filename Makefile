# Makefile for YADRTA Projects
SHELL := /bin/bash

# Django Variables
# -------------------------------------------------------------------------------------
VENV		:= ./.venv
ENVS		:= ./.envs
BIN		:= $(VENV)/bin
PYTHON3		:= $(BIN)/python3
PYTHON		:= $(PYTHON3)

# Local environment variables for Django
include $(ENVS)/.local/.django
include $(ENVS)/.local/.postgres

.PHONY: help venv install migrate startproject runserver django-shell db-up db-shell test coverage travis

.DEFAULT_GOAL := runserver

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# LOCAL DEV
# -------------------------------------------------------------------------------------

# Install Project
# -------------------------------------------------------------------------------------
venv: ## Make a new virtual environment
	# python3 -m venv $(VENV) && source $(BIN)/activate
	virtualenv -p python3.8 $(VENV) && source $(BIN)/activate

install: venv ## Make venv and install local requirements
	$(BIN)/pip install -r requirements/local.txt

migrate: ## Make migrate
	$(PYTHON) manage.py migrate

startproject: install migrate ## Install requirements, apply migrations

makemigrations: ## Make migrations
	$(PYTHON) manage.py makemigrations

allmigrations: makemigrations migrate ## Make migrations and migrate

createsecret: ## Create DJANGO_SECRET
	@echo "Creating SECRET_KEY"
	@echo "SECRET_KEY="\"`python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'`\"

# Create a super user from env var
# You need to define an env var : DJANGO_DEV_ADMIN_LOCAL. Example below
# DJANGO_DEV_ADMIN_LOCAL=name:email:password
# DJANGO_DEV_ADMIN_LOCAL=testadmin:testadmin@testapi.com:123asX3?23
# Or Make get it from .envs/.local/.django
create-superuser: ## Create local django admin user.
	@echo "from django.contrib.auth import get_user_model;"\
		"User = get_user_model();" \
		"User.objects.create_superuser(*'$(DJANGO_DEV_ADMIN_LOCAL)'.split(':'))" \
		| $(PYTHON) manage.py shell

# Django
# -------------------------------------------------------------------------------------
django-shell: ## Run ipython in django shell
	$(PYTHON) manage.py shell -i ipython

runserver: ## Run the Django server
	$(PYTHON) manage.py runserver $(DJANGO_PORT)

# TEST
# -------------------------------------------------------------------------------------
_test: ## Run spesific tests. Test runner is pytest
	pytest tests/vone/test_views.py::TestTagDetailView
	# pytest tests/vone/test_views.py::TestTagCreateAPIView

coverage: ## Clear and run coverage report
	coverage erase
	coverage run -m pytest
	coverage report -m
	coverage html

test: coverage ## Run tests and make coverage report

# DOCKER
# -------------------------------------------------------------------------------------
# Local
docker-build: ## Start the Docker containers in the background
	docker-compose -f local.yml build

docker-up: ## Start the Docker containers in the background
	docker-compose -f local.yml up -d

docker-start: ## Start the Docker containers in the background
	docker-compose -f local.yml start

docker-stop: ## Start the Docker containers in the background
	docker-compose -f local.yml stop

db-shell: ## Access the Postgres Docker database interactively with psql
	docker exec -it $(DBCONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

echo-docker: ## Ensure Local DB option
	@echo "$(USE_DOCKER)"
