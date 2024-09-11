import pytest
import requests_mock
import urllib.parse
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from typing import Optional

from gdpr.consts import CLEARED_VALUE
from gdpr.service import clear_data
from gdpr.tests.conftest import get_api_token_for_user_with_scopes
from occurrences.factories import (
    EnrolmentFactory,
    EventQueueEnrolmentFactory,
    StudyGroupFactory,
    StudyLevelFactory,
)
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)

User = get_user_model()


def _request_gdpr_delete(
    user,
    id_value,
    scopes=(settings.GDPR_API_DELETE_SCOPE,),
    query_params=None,
    data=None,
):
    gdpr_api_client = APIClient()

    with requests_mock.Mocker() as req_mock:
        auth_header = get_api_token_for_user_with_scopes(user, scopes, req_mock)
        gdpr_api_client.credentials(HTTP_AUTHORIZATION=auth_header)

        if query_params:
            query = "?" + urllib.parse.urlencode(query_params)
        else:
            query = ""

        request_kwargs = {"format": "json"}
        if data:
            request_kwargs["data"] = data

        return gdpr_api_client.delete(
            reverse(
                "helsinki_gdpr:gdpr_v1",
                kwargs={settings.GDPR_API_MODEL_LOOKUP: id_value},
            )
            + query,
            **request_kwargs,
        )


def _assert_clear(user, original_password: Optional[str] = None):
    if original_password:
        assert user.password != original_password
    assert user.first_name == ""
    assert user.last_name == ""
    assert user.email == ""
    assert user.username == f"{CLEARED_VALUE}-{user.uuid}"


def _delete_user(user, params):
    assert User.objects.count() == 1
    response = _request_gdpr_delete(user, user.uuid, **params)
    assert response.status_code == 204
    assert User.objects.count() == 1


def _assert_person_with_all_data_relations_populated(person):
    assert person.organisations.count() > 0
    assert person.organisationproposal_set.count() > 0
    assert person.studygroup_set.count() > 0
    assert person.eventqueueenrolment_set.count() > 0
    assert person.enrolment_set.count() > 0


def _test_person_with_all_data_relations_populated(user, assert_counts=True):
    person = PersonFactory(user=user, organisations=[OrganisationFactory()])

    OrganisationProposalFactory(applicant=person)

    study_levels = StudyLevelFactory.create_batch(3)
    # Person has 2 groups
    group1, group2 = StudyGroupFactory.create_batch(
        2, person=person, study_levels=study_levels
    )
    # Person has 2 enrolments which occurrences are related to the event for group 1
    EnrolmentFactory.create_batch(2, person=person, study_group=group1)
    # Person has 1 enrolment which occurrence is related to the event for group 2
    enrolment = EnrolmentFactory(person=person, study_group=group2)
    # There are some other enrolments also made by unknown persons
    EnrolmentFactory.create_batch(5, occurrence=enrolment.occurrence)
    # Person is also in queue to the p_event where there are some enrolments already
    EventQueueEnrolmentFactory(study_group=group1, person=person)
    if assert_counts:
        _assert_person_with_all_data_relations_populated(person)


@pytest.mark.django_db
def test_clear_data_service(user):
    original_password = user.password
    clear_data(user=user, dry_run=False)
    user.refresh_from_db()
    _assert_clear(user, original_password)


@pytest.mark.django_db
@pytest.mark.parametrize("key", ["data", "query_params"])
def test_gdpr_api_delete_profile_dry_run(true_value, user, key):
    email = user.email
    assert email != ""
    _delete_user(user, {key: {"dry_run": true_value}})
    user.refresh_from_db()
    assert user.email == email
    assert User.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("key", ["data", "query_params"])
def test_gdpr_api_delete_profile(false_value, user, key):
    original_password = user.password
    _delete_user(user, {key: {"dry_run": false_value}})
    user.refresh_from_db()
    _assert_clear(user, original_password)


@pytest.mark.django_db
def test_gdpr_api_delete_profile_no_params(user):
    original_password = user.password
    _delete_user(user, {})
    user.refresh_from_db()
    _assert_clear(user, original_password)


@pytest.mark.django_db
def test_gdpr_api_user_not_found(user):
    """The response with a status code 204 is given in the case
    that the service does not contain any data for the profile
    or is completely unaware of the identified profile.

    See more: https://profile-api.dev.hel.ninja/docs/gdpr-api/
    """
    assert User.objects.count() == 1
    response = _request_gdpr_delete(user=user, id_value=uuid.uuid4())
    assert response.status_code == 204
    assert User.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_scope", ["simplest", "most_complex"])
def test_get_profile_data_from_gdpr_api(
    test_scope, snapshot, gdpr_api_client, requests_mock, user, mock_get_event_data
):
    user.last_login = timezone.now()
    user.save()

    if test_scope == "most_complex":
        _test_person_with_all_data_relations_populated(user, assert_counts=True)

    auth_header = get_api_token_for_user_with_scopes(
        user, [settings.GDPR_API_QUERY_SCOPE], requests_mock
    )
    gdpr_api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = gdpr_api_client.get(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: user.uuid},
        )
    )
    assert response.status_code == 200
    snapshot.assert_match(response.json())


@pytest.mark.django_db
def test_delete_profile_data_from_gdpr_api(user, gdpr_api_client, requests_mock):
    auth_header = get_api_token_for_user_with_scopes(
        user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    gdpr_api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = gdpr_api_client.delete(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: user.uuid},
        )
    )
    assert response.status_code == 204
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username=user.username)


@pytest.mark.django_db
def test_gdpr_api_requires_authentication(user, gdpr_api_client):
    response = gdpr_api_client.get(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: user.uuid},
        )
    )
    assert response.status_code == 401

    response = gdpr_api_client.delete(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: user.uuid},
        )
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_can_only_access_his_own_profile(user, gdpr_api_client, requests_mock):
    auth_header = get_api_token_for_user_with_scopes(
        user,
        [settings.GDPR_API_QUERY_SCOPE, settings.GDPR_API_DELETE_SCOPE],
        requests_mock,
    )
    gdpr_api_client.credentials(HTTP_AUTHORIZATION=auth_header)

    another_user = UserFactory()
    response = gdpr_api_client.get(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: another_user.uuid},
        )
    )
    assert response.status_code == 403

    response = gdpr_api_client.delete(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={settings.GDPR_API_MODEL_LOOKUP: another_user.uuid},
        )
    )
    assert response.status_code == 403
