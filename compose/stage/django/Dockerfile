FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/stage.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/stage/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Adds our application code to the image
COPY . app
WORKDIR app

EXPOSE 8000

ENTRYPOINT ["/entrypoint"]
