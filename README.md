# Beta Kultus API

[![status](https://travis-ci.com/City-of-Helsinki/palvelutarjotin.svg)](https://github.com/City-of-Helsinki/palvelutarjotin)
[![codecov](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin/branch/develop/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin)


## Environments
Production environment:
- TBA

Testing environment:
- https://palvelutarjotin-admin.test.kuva.hel.ninja/

## Development with Docker

1. Copy `docker-compose.env.yaml.example` to `docker-compose.env.yaml` and modify it if needed.

2. Run `docker-compose up`

The project is now running at [localhost:8081](http://localhost:8081)

## Development without Docker

Prerequisites:

* PostgreSQL 10
* Python 3.7

### Installing Python requirements

* Run `pip install -r requirements.txt`
* Run `pip install -r requirements-dev.txt` (development requirements)

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S palvelutarjotin  # use password `palvelutarjotin`
    sudo -u postgres createdb -O palvelutarjotin palvelutarjotin

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER palvelutarjotin CREATEDB;"
    

### Daily running, Debugging

* Create `.env` file: `touch .env` or make a copy of `.env.example` 
* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `python manage.py runserver localhost:8081`
* The project is now running at [localhost:8081](http://localhost:8081)

### Configuration

1. You must config Beta Kultus API to integrate with [LinkedEvent API](https://github.com/City-of-Helsinki
/linkedevents)
    
    Add the following lines to your local `.env` 
    ```python
    LINKED_EVENTS_API_ROOT=<your_linked_event_api_url>
    LINKED_EVENTS_API_KEY=<your_linked_event_api_key>
    LINKED_EVENTS_DATA_SOURCE=<your_linked_event_data_source>
    ```
    If you are not using local Linked Event, as administrator to provide these information.
    
    If you installed LinkedEvent yourself, you can create API_KEY and DATA_SOURCE from your local LinkedEvent admin
    interface (Checkout the how to setup local LinkedEvent [here](https://github.com/City-of-Helsinki/linkedevents#how-to-setup-your-local-development-environment))

2. (Optional) To use the SMS notification functionality, you have to acquire the API_KEY from [Notification Service API
](https://github.com/City-of-Helsinki/notification-service-api) then add these lines to your local `.env`

    ```python
    NOTIFICATION_SERVICE_API_TOKEN=your_api_key
    NOTIFICATION_SERVICE_API_URL=notification_service_end_point
    ```
 

## API Documentation
To view the API documentation, in DEBUG mode visit: http://localhost:8081/graphql and checkout the `Documentation Explorer` section

## Keeping Python requirements up to date

1. Install `pip-tools`:

    * `pip install pip-tools`

2. Add new packages to `requirements.in` or `requirements-dev.in`

3. Update `.txt` file for the changed requirements file:

    * `pip-compile requirements.in`
    * `pip-compile requirements-dev.in`

4. If you want to update dependencies to their newest versions, run:

    * `pip-compile --upgrade requirements.in`

5. To install Python requirements run:

    * `pip-sync requirements.txt`

## Code format

This project uses [`black`](https://github.com/ambv/black) for Python code formatting.
We follow the basic config, without any modifications. Basic `black` commands:

* To let `black` do its magic: `black .`
* To see which files `black` would change: `black --check .`

Or you can use [`pre-commit`](https://pre-commit.com/) to quickly format your code before committing.


1. Install `pre-commit` (there are many ways to do but let's use pip as an example):
    * `pip install pre-commit`
2. Set up git hooks from `.pre-commit-config.yaml`, run this command from project root:
    * `pre-commit install`

After that, formatting hooks will run against all changed files before committing

## Contact infomation

@quyenlq

## Issues board

https://helsinkisolutionoffice.atlassian.net/projects/PT/issues
