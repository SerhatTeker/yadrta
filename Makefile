SHELL := /bin/bash

.PHONY: runserver createsuperuser

.DEFAULT_GOAL := runserver

runserver:
	python todo/manage.py runserver 8000

allmigrations: migrations migrate

migrate:
	./todo/manage.py migrate
migrations:
	./todo/manage.py makemigrations
# Create a super user from env var
# You need to define an env var : DJANGO_DEV_ADMIN. Example below
# DJANGO_DEV_ADMIN=name:email:password
# DJANGO_DEV_ADMIN=user@test.api:user@test.api:123asX3?23
createsuperuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(*'${DJANGO_DEV_ADMIN}'.split(':'))" | python todo/manage.py shell
# Create a SECRET_KEY for settings
createsecret:
	python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
