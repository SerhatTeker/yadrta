[![license](https://img.shields.io/badge/license-bsd%203--clause-blue.svg)](https://opensource.org/licenses/bsd-3-clause)

# # Django Rest Todo - ATDA

Another todo app using django rest and django with openapi specification.

![openapi - swagger](./docs/img/screenshots/swagger.png)
_swagger_

![openapi - redoc](./docs/img/screenshots/redoc.png)
_redoc_

![django rest](./docs/img/screenshots/drf.png)
_django rest api_

## ## Getting Started

This app gets requests from `localhost` on port `8000` and performs __CRUD__
operations.

<!-- `GET` `PUT` `DELETE` `POST` -->

Base endpoints are:
- The base endpoint is: http://localhost:8000
- `BASE_URL` for `api` is `/api/v1/`

CRUD api endpoints:
- `/api/v1/category/`
- `/api/v1/tag/`
- `/api/v1/todo/`

For documemtation:
- `/api/v1/swagger/`
- `/api/v1/swagger.yaml`
- `/api/v1/swagger.json`
- `/api/v1/redoc/`


### ### Prerequisites

- Python 3.8

### ### Installing

Clone the repo with `ssh`:

```bash
$ git clone https://github.com/SerhatTeker/django-rest-todo.git
```

or with `https`:

```bash
$ git clone git@github.com:SerhatTeker/django-rest-todo.git
```

### ### Getting Up and Running Locally

#### #### Setting Up Development Environment

1. Create a virtualenv:

    ```bash
    $ virtualenv -p python3.8 .venv
    ```

2. Activate the virtualenv you have just created:

    ```bash
    $ source .venv/bin/activate
    ```

3.  Install development requirements:

    ```bash
    $ pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    $ python manage.py migrate
    ```

5. Run Django development server:

    ```bash
    $ python manage.py runserver 8000
    ```

    or you can use __Makefile__:

    ```bash
    $ make runserver
    # or shorter : default make target is `runserver`
    # $ make
    ```

#### #### Setting Up Development Environment



#### #### Summary

Congratulations, you have made it!

<!--
## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
-->

## Usage

<!--
## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read
[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for
details on our code of conduct, and the process for submitting pull requests to
us.
-->

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Serhat Teker** - *Initial work* - [serhatteker](https://github.com/serhatteker)

<!-- See also the list of
[contributors](https://github.com/your/project/contributors) who participated in
this project. -->

## License

This project is licensed under the BSD-3-Clause License - see the
[LICENSE.md](LICENSE.md) file for details.
