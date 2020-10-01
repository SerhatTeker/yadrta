FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements/base.txt ./requirements/base.txt
COPY ./requirements/production.txt ./requirements/production.txt
RUN pip install -r ./requirements/production.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - config.wsgi:application
