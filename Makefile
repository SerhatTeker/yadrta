# Makefile for YADRTA Projects
SHELL := /bin/bash

# Django Variables
# -------------------------------------------------------------------------------------
VENV		:= ./.venv
BIN		:= $(VENV)/bin
PYTHON3		:= $(BIN)/python3
PYTHON		:= $(PYTHON3)
DJANGO_PORT	:= 8000
DBNAME		:= "yadrta"

include .env

.PHONY: help venv install migrate startproject runserver django-shell db-up db-shell test coverage

.DEFAULT_GOAL := runserver

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# INSTALL PROJECT
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
# You need to define an env var : DJANGO_DEV_ADMIN. Example below
# DJANGO_DEV_ADMIN=name:email:password
# DJANGO_DEV_ADMIN=testadmin:testadmin@testapi.com:123asX3?23
createsuperuser: ## Create django admin user. Before define $DJANGO_DEV_ADMIN in .env or environment
	@echo "from django.contrib.auth import get_user_model;"\
		"User = get_user_model();" \
		"User.objects.create_superuser(*'$(DJANGO_DEV_ADMIN)'.split(':'))" \
		| python manage.py shell

createsuperuser-man: ## Create manually django admin. Asks password
	$(PYTHON) manage.py createsuperuser --email testadmin@testapi.com --username testadmin

# LOCAL DEV
# -------------------------------------------------------------------------------------
django-shell: ## Run ipython in django shell
	python manage.py shell -i ipython

runserver: ## Run the Django server
	$(PYTHON) manage.py runserver $(DJANGO_PORT)

# TEST
# -------------------------------------------------------------------------------------
test: ## Run tests. Test runner is pytest
	pytest tests/vone/test_views.py::TestTagDetailView
	# pytest tests/vone/test_views.py::TestTagCreateAPIView

coverage: ## Clear and run coverage report
	coverage erase
	coverage run -m pytest
	coverage report -m
	coverage html

# DOCKER
# -------------------------------------------------------------------------------------
db-up: ## Start the Docker containers in the background
	docker-compose up -d

db-shell: ## Access the Postgres Docker database interactively with psql
	docker exec -it container_name psql -d $(DBNAME)
