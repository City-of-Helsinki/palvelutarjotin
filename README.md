# Beta Kultus API

[![status](https://travis-ci.com/City-of-Helsinki/palvelutarjotin.svg)](https://github.com/City-of-Helsinki/palvelutarjotin)
[![codecov](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin/branch/develop/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin)

## Environments

Production environment:

- https://api.hel.fi/kultus-beta/graphql

Testing environment:

- https://palvelutarjotin-api.test.kuva.hel.ninja/graphql

## Development with Docker

1. Copy `docker-compose.env.yaml.example` to `docker-compose.env.yaml` and modify it if needed.

2. Run `docker-compose up`

The project is now running at [localhost:8081](http://localhost:8081)

## Development without Docker

Prerequisites:

- PostgreSQL 10
- Python 3.7

### Installing Python requirements

- Run `pip install -r requirements.txt`
- Run `pip install -r requirements-dev.txt` (development requirements)

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S palvelutarjotin  # use password `palvelutarjotin`
    sudo -u postgres createdb -O palvelutarjotin palvelutarjotin

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER palvelutarjotin CREATEDB;"

### Daily running, Debugging

- Create `.env` file: `touch .env` or make a copy of `.env.example`
- Set the `DEBUG` environment variable to `1`.
- Run `python manage.py migrate`
- Run `python manage.py runserver localhost:8081`
- The project is now running at [localhost:8081](http://localhost:8081)

### Configuration

1.  You must config Beta Kultus API to integrate with [LinkedEvent API](https://github.com/City-of-Helsinki/linkedevents)

    Add the following lines to your local `.env` or `docker-compose.env.yaml` if you are using Docker. Take a look
    at the `.env.example` or `docker-compose.env.yaml.example` to see list of required variables

    ```python
    LINKED_EVENTS_API_ROOT=<your_linked_event_api_url>          # e.g. http://localhost:8000/v1/
    LINKED_EVENTS_API_KEY=<your_linked_event_api_key>           # a value from an Api key -field in a LinkedEvent data source.
    LINKED_EVENTS_DATA_SOURCE=<your_linked_event_data_source>   # e.g. local-kultus
    ```

    - If you are not using local Linked Event, contact LinkedEvent team to provide these information.

    - If you installed LinkedEvent yourself, you can create API_KEY and DATA_SOURCE from your local LinkedEvent admin
      interface

    - For example: Assuming you are running LinkedEvent API in port 8080 and Kultus API using port 8081, go here to
      create your DATA_SOURCE and get the API key:
      http://path_to_your_linked_event/admin/events/datasource/add/

2.  Create superuser:

    - If you run the Kultus API using Docker, by default one superuser will be created with username `admin`, password
      `admin`
    - If you run the Kultus API in your local env, run this command from the project root to create superuser:

    ```
    ./manage.py add_admin_user -u <username> -p <password> -e <email-address>
    ```

    Then you can use this account to login to Kultus API admin interface at for example http://path_to_your_kultus_api/admin

3.  Create Provider Organisation

    - It's required to create at least one organisation from LE and Kultus. This will be used on Provider UI where user
      can pick their organisation after login. You'll have to create an organisation in LE, then copy the information
      to Kultus.

    - If you run the default importer in LE, there will be already some organisations created there, you can use them
      instead of create your own organisation, but it's recommended to create new one
    - To create new organisation in LE, visit: http://path_to_your_linked_eventadmin/django_orghierarchy/organization/add/
    - After creating Organisation in LE, create a similar one in Kultus by visit: http://localhost:8000/admin/organisations/organisation/add/
      In the `publisher_id` field, use the organisation ID that you got from new LE organsation (e.g ahjo:u4804001010)

4.  Create/update event permissions

    - If you only want to work with the GraphQL API without using UI (Teacher UI and Provider UI), when running the
      API in debug mode, there will be a GraphQL client already available at http://path_to_your_kultus_api/graphql
      where you can run your graphql query/mutation. Note that in order to execute mutation or some query requires
      authentication. In that case, you'll have to login to the admin interface at the beginning of your session
      , after that you can use that session to run graphql mutation in http://path_to_your_kultus_api/graphql
    - To be able to manage events via Provider UI, you have to log in the Provider UI first, and create an user there
      . You'll have to input some information and select the organsation from the organisation list that you created in
      step 2. After that, login to the Kultus-API admin interface using the superuser account, find the new user and
      assign staff permission to this user. After that the user can create/edit events from Provider UI

5.  Configuration needed to use Provider UI and Teacher UI locally:
    - There are some required variables need to be create and config locally. They are the keyword set ids which will
      be used to populate the data of some select boxes in the UI. You'll have to create the KeywordSet in LE, add
      some Keywords to the KeywordSet, then set the KeywordSet ids to `.env` or `docker-compose.env.yaml` depends on
      what you are using.
      - Create three keyword sets in LE using this address: http://path_to_your_linked_event/admin/events/keywordset
        / with the following name: `Kultus Targer Groups`, `Kultus Additional Criteria`, `Kultus Categories`
      - Add some Keywords to all aboves KeywordSets. There should be some keywords already available in the system if you
        run the required importers in LinkedEvent. Or you can create new keywords yourself.
      - Get the ID of those keyword set and put them in `.env` or `docker-compose.env.yaml` depends on your local
        ```python
          KEYWORD_SET_CATEGORY_ID=qq:kultus:categories
          KEYWORD_SET_ADDITIONAL_CRITERIA_ID=qq:kultus:additional_criteria
          KEYWORD_SET_TARGET_GROUP_ID=qq:kultus:target_groups
        ```
6.  (Optional) To use the SMS notification functionality, you have to acquire the API_KEY from [Notification Service API
    ](https://github.com/City-of-Helsinki/notification-service-api) then add these lines to your local `.env` / `.docker -compose.env.yaml`

        ```python
        NOTIFICATION_SERVICE_API_TOKEN=your_api_key
        NOTIFICATION_SERVICE_API_URL=notification_service_end_point
        ```

7.  (Optional) To offer neighborhood division through a GraphQL API, the Neighborhood API needs to be configured. By default it is using kartta.hel.fi open data API and it should work out of the box.

        ```python
        NEIGHBORHOOD_API_ROOT=https://kartta.hel.fi/ws/geoserver/avoindata/wfs
        ```

8.  (Optional) The notification templates can be imported via
    a. a Google sheet importer
    b. a Template file importer

The importer can be used to create and update the notification templates or to check whether the templates are in sync.
The importer can be used via Django management commands (in notification_importers app) or admin site tools.

To enable admin site tools, some configuration is needed:

To enable a selected importer (`NotificationFileImporter` or `NotificationGoogleSheetImporter`)

```python
NOTIFICATIONS_IMPORTER = (
    "notification_importers.notification_importer.NotificationFileImporter"
)
```

If a Google sheet importer is used, also `NOTIFICATIONS_SHEET_ID` is needed

```python
NOTIFICATIONS_SHEET_ID = "1234"
```

If a File importer is used, files should be stored in notification_importers app in notification_importers/templates/sms and notification_importers/templates/email folders.
There is also a naming convention used there. The file name must be given in this pattern [notification_type]-[locale].[html|j2].

## API Documentation

To view the API documentation, in DEBUG mode visit: http://localhost:8081/graphql and checkout the `Documentation Explorer` section

## Keeping Python requirements up to date

1. Install `pip-tools`:

   - `pip install pip-tools`

2. Add new packages to `requirements.in` or `requirements-dev.in`

3. Update `.txt` file for the changed requirements file:

   - `pip-compile requirements.in`
   - `pip-compile requirements-dev.in`

4. If you want to update dependencies to their newest versions, run:

   - `pip-compile --upgrade requirements.in`

5. To install Python requirements run:

   - `pip-sync requirements.txt`

## Code format

This project uses [`black`](https://github.com/ambv/black) for Python code formatting.
We follow the basic config, without any modifications. Basic `black` commands:

- To let `black` do its magic: `black .`
- To see which files `black` would change: `black --check .`

Or you can use [`pre-commit`](https://pre-commit.com/) to quickly format your code before committing.

1. Install `pre-commit` (there are many ways to do but let's use pip as an example):
   - `pip install pre-commit`
2. Set up git hooks from `.pre-commit-config.yaml`, run this command from project root:
   - `pre-commit install`

After that, formatting hooks will run against all changed files before committing

## Contact infomation

@quyenlq @nikomakela

## Issues board

https://helsinkisolutionoffice.atlassian.net/projects/PT/issues
