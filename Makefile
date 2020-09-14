django:
	./todo/manage.py runserver 8000

allmigrations: migrations migrate

migrate:
	./todo/manage.py migrate
migrations:
	./todo/manage.py makemigrations

