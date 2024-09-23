# Kultus API

[![status](https://travis-ci.com/City-of-Helsinki/palvelutarjotin.svg)](https://github.com/City-of-Helsinki/palvelutarjotin)
[![codecov](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin/branch/develop/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/palvelutarjotin)

## Environments

Production environment:

- https://kultus.api.hel.fi/graphql
- Triggered by creation of release-\* tag, e.g. `release-v0.1.0`
  - Needs to be manually approved in pipeline to be deployed

Staging environment:

- https://kultus.api.stage.hel.ninja/graphql
- Automatically deployed by creation of release-\* tag, e.g. `release-v0.1.0`

Testing environment:

- https://kultus.api.test.hel.ninja/graphql
- Automatically deployed by any change to master branch

## Development with Docker

1. Copy `docker-compose.env.yaml.example` to `docker-compose.env.yaml` and modify it if needed.
2. Configure settings, see [Configuration](#configuration)
3. Run `docker-compose up`

The project is now running at http://localhost:8081

## Development without Docker

Prerequisites:

- PostgreSQL 10
- Python 3.11

Steps:

1. Install Python requirements, see [Installing Python requirements](#installing-python-requirements)
2. Setup database, see [Database](#database)
3. Configure settings, see [Configuration](#configuration)
4. Run the server, see [Daily running, Debugging](#daily-running-debugging)

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
- The project is now running at http://localhost:8081

## Configuration

1.  You must config Kultus API to integrate with [LinkedEvents API](https://github.com/City-of-Helsinki/linkedevents)

    Add the following lines to your local `.env` or `docker-compose.env.yaml` if you are using Docker. Take a look
    at the `.env.example` or `docker-compose.env.yaml.example` to see list of required variables

    ```python
    LINKED_EVENTS_API_ROOT=<your_linked_event_api_url>          # e.g. http://localhost:8000/v1/
    LINKED_EVENTS_API_KEY=<your_linked_event_api_key>           # value from Api key field in LinkedEvents data source
    LINKED_EVENTS_DATA_SOURCE=<your_linked_event_data_source>   # e.g. local-kultus
    ```

    - If you are not using local Linked Event, contact LinkedEvents team to provide these information.

      - Or you may find them on Azure DevOps if you have access to [kultus](https://dev.azure.com/City-of-Helsinki/kultus/):
        - From [Kultus API testing variables](https://dev.azure.com/City-of-Helsinki/kultus/_git/kultus-pipelines?path=/variables/kultus-api-testing.yml):
          - LINKED_EVENTS_API_ROOT=https://linkedevents.api.test.hel.ninja/v1/
          - LINKED_EVENTS_DATA_SOURCE=kultus
        - LINKED_EVENTS_API_KEY secret from:
          - [Kultus testing keyvault library](https://dev.azure.com/City-of-Helsinki/kultus/_library?itemType=VariableGroups&view=VariableGroupView&variableGroupId=3458&path=testing-kv)
            - [Microsoft Azure keyvaults with kultus tag](https://portal.azure.com/#view/HubsExtension/BrowseResourcesWithTag/tagName/project/tagValue/kultus)
              - [hki-LLvCIhJC-test-kv keyvault secrets](https://portal.azure.com/#@helsinginkaupunki.onmicrosoft.com/resource/subscriptions/5050c890-3cab-451b-b763-ad55ff3688de/resourceGroups/hki-kanslia-shared-we-devtest-rg/providers/Microsoft.KeyVault/vaults/hki-LLvCIhJC-test-kv/secrets)
                - [LINKED-EVENTS-API-KEY secret](https://portal.azure.com/#@helsinginkaupunki.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://hki-llvcihjc-test-kv.vault.azure.net/secrets/LINKED-EVENTS-API-KEY/93e659586e5145bda88ccde1a9195c66)

    - If you installed LinkedEvents yourself, you can create API_KEY and DATA_SOURCE from your local LinkedEvents admin
      interface at http://path_to_your_linked_events/admin/events/datasource/add/

2.  Create superuser:

    - If you run the Kultus API using Docker, first enter the backend container using
      `docker exec -it kukkuu-backend bash` and run the next command inside the container
    - Run this command from the project root to create superuser:

      ```
      python manage.py add_admin_user -u <username> -p <password> -e <email-address>
      ```

    Then you can use this account to login to Kultus API admin interface at for example
    http://path_to_your_kultus_api/admin

3.  Create Provider Organisation

    - At least a single organisation is required to be present in LinkedEvents and in Kultus.
    - This will be used on Provider UI where user can pick their organisation after login.
    - If you don't have an organisation in LinkedEvents yet you should create one.
    - In case you're using an existing [LinkedEvents testing environment](https://linkedevents.api.test.hel.ninja/v1/) you
      can just pick one of the `id` values from the [organisation list](https://linkedevents.api.test.hel.ninja/v1/organization/),
      e.g. [ahjo:u4804001010](https://linkedevents.api.test.hel.ninja/v1/organization/ahjo:u4804001010/)
    - In case you've setup LinkedEvents locally and don't have an existing organisation:
      - If you run the default importer in LinkedEvents, there will be already some organisations created there, you can
        use them instead of create your own organisation, but it's recommended to create new one
      - To create new organisation in LinkedEvents, visit:
        http://path_to_your_linked_events/admin/django_orghierarchy/organization/add/
      - Before adding organization, you must first create a data source as instructed earlier. You must also set the
        value to true for `objects may be edited by users` so that the data source can be selected for the organization.
    - After you have an organisation in LinkedEvents, create a similar one in Kultus at
      http://localhost:8081/admin/organisations/organisation/add/
      - Name: \<name of the organisation in LinkedEvents\>, e.g. `Kaupunginkirjasto`
      - Phone number: Can be left empty
      - Type: `Provider`
      - Persons: Can be left empty
      - Publisher id: \<id of the organisation in LinkedEvents\>, e.g. `ahjo:u4804001010`

4.  Create/update event permissions

    - If you only want to work with the GraphQL API without using UI (Teacher UI and Provider UI), when running the
      API in debug mode, there will be a GraphQL client already available at http://path_to_your_kultus_api/graphql
      where you can run your graphql query/mutation. Note that in order to execute mutation or some query requires
      authentication. In that case, you'll have to login to the admin interface at the beginning of your session,
      after that you can use that session to run graphql mutation in http://path_to_your_kultus_api/graphql
    - To be able to manage events via Provider UI, you have to log in the Provider UI first, and create an user there.
      You'll have to input some information and select the organisation from the organisation list that you created in
      step 2. After that, login to the Kultus-API admin interface using the superuser account, find the new user and
      assign staff permission to this user. After that the user can create/edit events from Provider UI

5.  Configuration needed to use Provider UI and Teacher UI locally:
    - These keyword set variables need to be configured in order to populate dropdown boxes' data in the UI:
      - KEYWORD_SET_CATEGORY_ID
      - KEYWORD_SET_TARGET_GROUP_ID
      - KEYWORD_SET_ADDITIONAL_CRITERIA_ID
    - In case you're using an existing [LinkedEvents testing environment](https://linkedevents.api.test.hel.ninja/v1/) you
      can just use the existing keyword sets i.e.
      [kultus:categories](https://linkedevents.api.test.hel.ninja/v1/keyword_set/kultus:categories/),
      [kultus:target_groups](https://linkedevents.api.test.hel.ninja/v1/keyword_set/kultus:target_groups/) and
      [kultus:additional_criteria](https://linkedevents.api.test.hel.ninja/v1/keyword_set/kultus:additional_criteria/)
      by setting the following variables in your `.env` or `docker-compose.env.yaml` file:
      ```python
      KEYWORD_SET_CATEGORY_ID=kultus:categories
      KEYWORD_SET_TARGET_GROUP_ID=kultus:target_groups
      KEYWORD_SET_ADDITIONAL_CRITERIA_ID=kultus:additional_criteria
      ```
    - In case you've setup LinkedEvents locally and don't have existing keyword sets:
      - You'll have to create the KeywordSet in LinkedEvents, add some Keywords to the KeywordSet, then set the
        KeywordSet ids to `.env` or `docker-compose.env.yaml` depending on which you are using.
        - Create three keyword sets in LinkedEvents using this address:
          http://path_to_your_linked_event/admin/events/keywordset / with the following name:
          `Kultus Targer Groups`, `Kultus Additional Criteria`, `Kultus Categories`
        - Add some Keywords to all aboves KeywordSets. There should be some keywords already available in the system if
          you run the required importers in LinkedEvents. Or you can create new keywords yourself.
        - Get the IDs of those keyword sets and put them in `.env` or `docker-compose.env.yaml` depending on which you
          are using
          ```python
            KEYWORD_SET_CATEGORY_ID=kultus:categories
            KEYWORD_SET_ADDITIONAL_CRITERIA_ID=kultus:additional_criteria
            KEYWORD_SET_TARGET_GROUP_ID=kultus:target_groups
          ```
6.  (Optional) To use the SMS notification functionality, you have to acquire the API_KEY from
    [Notification Service API](https://github.com/City-of-Helsinki/notification-service-api) and
    then add these lines to your local `.env` / `.docker -compose.env.yaml`:

    ```python
    NOTIFICATION_SERVICE_API_TOKEN=your_api_key
    NOTIFICATION_SERVICE_API_URL=notification_service_end_point
    ```

7.  (Optional) The notification templates can be imported via

    - a) Google sheet importer
    - b) Template file importer

    The importer can be used to create and update the notification templates or to check whether they are in sync.
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

    If a File importer is used, files should be stored in notification_importers app in
    notification_importers/templates/sms and notification_importers/templates/email folders.
    There is also a naming convention used there. The file name must be given in this pattern
    [notification_type]-[locale].[html|j2].

8.  (Optional) To offer Kindergartens, schools and colleges from the Servicemap of the Helsinki, the Servicemap API
    needs to be configured. By default it is using the open data from https://www.hel.fi/palvelukarttaws/rest/v4/unit/ and it
    should work out of the box.

```python
  env = environ.Env(
    SERVICEMAP_API_ROOT=(str, "https://www.hel.fi/palvelukarttaws/rest/v4/unit/"),
  )
  SERVICEMAP_API_CONFIG = {"ROOT": env.str("SERVICEMAP_API_ROOT")}
```

## API Documentation

To view the API documentation, in DEBUG mode visit http://localhost:8081/graphql and checkout the
`Documentation Explorer` section

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

## Maintaining

### Enrolment reports

_Enrolment report instances are for data utilizing. They are provided through a JSON view used by external parties. The
external parties will need credentials that has the enrolment report view permission to use the view!

Enrolment reports should maintain themselves automatically with nightly running cronjobs, but sometimes some manual
syncing might be needed. There are some tools for that in enrolment reports admin page:

- Sync unsynced enrolment reports -button can be used to create all the missing enrolment reports and to sync all the
  enrolment reports out of sync after the date of the last sync done. If the date of the last sync is greater than the
  updated_at -field's value in an instance that needs the sync, the sync must be done by selecting the instance from
  admin list view and using the rehydrate -sync actions.
- Rehydrate the enrolment report instances with LinkedEvents data -action can be used to sync the enrolment report
  instance with the related enrolment instance. This action also fetches the data from LinkedEvents API, which can lead
  to some heavy API usage, so please use carefully. All the selected enrolment report instances will be affected.
- Rehydrate the enrolment report instances without LinkedEvents data -action can be used to sync the enrolment report
  instance with the related enrolment instance without fetching any data from the LinkedEvents API. This action should
  be used when the sync needs no data from LiknedEvents, for example when only the enrolment status is wanted to be
  updated.

Enrolment reports can be initialized with the same management command that the cronjob runs: `sync_enrolment_reports`.
It will create the missing enrolment reports and sync the enrolment report instances that are out of sync with the
related enrolment instance. The `sync_enrolment_reports` command takes in 2 optional parameters:

- --sync_from, which can be used to set the date of the updated_at -field that will be used to fetch the enrolments
  being handled in the sync process.
- --ignore_linkedevents, which can be used to prevent data fetching from LinkedEvents API.
