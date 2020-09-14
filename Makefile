django:
	./manage.py runserver 8000

allmigrations: migrations migrate

migrate:
	./manage.py migrate
migrations:
	./manage.py makemigrations

