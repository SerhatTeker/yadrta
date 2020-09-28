SHELL := /bin/bash

.PHONY: runserver createsuperuser

.DEFAULT_GOAL := runserver

runserver:
	python manage.py runserver 8000

allmigrations: migrations migrate

migrate:
	./manage.py migrate
migrations:
	./manage.py makemigrations

# Create a super user from env var
# You need to define an env var : DJANGO_DEV_ADMIN. Example below
# DJANGO_DEV_ADMIN=name:email:password
# DJANGO_DEV_ADMIN=testadmin:testadmin@testapi.com:123asX3?23
createsuperuser:
	@echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(*'${DJANGO_DEV_ADMIN}'.split(':'))" | python manage.py shell

# Asks password
createsuperuser-default:
	python manage.py createsuperuser --email testadmin@testapi.com --username testadmin

# Create a SECRET_KEY for settings
createsecret:
	@python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
pytest:
	# pytest tests/vone/test_tag_views.py::TestTagDetailTwoAPIView
	# pytest tests/vone/test_tag_views.py::TestTagDetailAPIView
	pytest tests/vone/test_tag_views.py::TestTrialBaseTestClass
