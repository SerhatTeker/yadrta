FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/stage.txt

# Adds our application code to the image
COPY . app
WORKDIR app

EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:8000 --access-logfile - config.wsgi:application
