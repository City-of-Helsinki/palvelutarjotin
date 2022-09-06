import pytest
from datetime import timedelta
from django.utils import timezone

from occurrences.factories import EnrolmentFactory
from occurrences.models import Enrolment
from verification_token.factories import EnrolmentVerificationTokenFactory
from verification_token.models import VerificationToken


@pytest.mark.django_db
def test_enrolment_verification_token_creation(mock_get_event_data):
    verification_token = EnrolmentVerificationTokenFactory()
    assert VerificationToken.objects.count() == 1
    assert verification_token.content_object.__class__ == Enrolment
    assert verification_token.key is not None


@pytest.mark.django_db
def test_verification_token_is_valid(mock_get_event_data):
    valid_token = EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() + timedelta(minutes=10)
    )
    invalid_token1 = EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() - timedelta(minutes=10)
    )
    invalid_token2 = EnrolmentVerificationTokenFactory(is_active=False)
    assert valid_token.is_valid() is True
    assert invalid_token1.is_valid() is False
    assert invalid_token2.is_valid() is False


@pytest.mark.django_db
def test_verification_token_filter_active_tokens(mock_get_event_data):
    token1 = EnrolmentVerificationTokenFactory(is_active=False)
    token2 = EnrolmentVerificationTokenFactory(is_active=True)
    token3 = EnrolmentVerificationTokenFactory(is_active=True, key="123")
    # Test active with a class
    assert all(
        token in [token2, token3]
        for token in VerificationToken.objects.filter_active_tokens(Enrolment)
    )
    # Test active with an instance
    assert token2 in VerificationToken.objects.filter_active_tokens(
        token2.content_object
    )
    # Test inactive with an instance
    assert (
        len(VerificationToken.objects.filter_active_tokens(token1.content_object)) == 0
    )
    # Test active with a class and key
    assert (
        len(
            [
                t.id
                for t in VerificationToken.objects.filter_active_tokens(
                    Enrolment, key="123"
                )
            ]
        )
        == 1
    )
    # Test with a person
    assert (
        len(
            VerificationToken.objects.filter_active_tokens(
                token2.content_object, person=token2.person
            )
        )
        == 1
    )


@pytest.mark.django_db
def test_verification_token_deactivation(mock_get_event_data):
    # Test with instance
    token1 = EnrolmentVerificationTokenFactory(is_active=True)
    VerificationToken.objects.deactivate_token(token1.content_object)
    token1 = VerificationToken.objects.get(pk=token1.id)
    assert token1.is_active is False

    # test with class and key
    token2 = EnrolmentVerificationTokenFactory(is_active=True)
    VerificationToken.objects.deactivate_token(Enrolment, key=token2.key)
    token2 = VerificationToken.objects.get(pk=token2.id)
    assert token2.is_active is False

    # Test with person
    token3 = EnrolmentVerificationTokenFactory(is_active=True)
    VerificationToken.objects.deactivate_token(
        token3.content_object, person=token3.person
    )
    token3 = VerificationToken.objects.get(pk=token3.id)
    assert token3.is_active is False

    # Test with wrong person
    token4 = EnrolmentVerificationTokenFactory(is_active=True)
    VerificationToken.objects.deactivate_token(
        token4.content_object, person=token3.person
    )
    token4 = VerificationToken.objects.get(pk=token4.id)
    assert token4.is_active is True

    # Test with verification_type
    token5 = EnrolmentVerificationTokenFactory(is_active=True)
    VerificationToken.objects.deactivate_token(
        token5.content_object,
        verification_type=token5.verification_type,
        person=token5.person,
    )
    token5 = VerificationToken.objects.get(pk=token5.id)
    assert token5.is_active is False


@pytest.mark.django_db
def test_verification_token_create_token_with_manager(mock_get_event_data):
    enrolment = EnrolmentFactory()
    person = enrolment.person
    email = "adsf@asdf.com"

    token1 = VerificationToken.objects.create_token(
        enrolment, person, VerificationToken.VERIFICATION_TYPE_CANCELLATION
    )
    assert token1.key is not None
    assert token1.content_object == enrolment
    assert token1.person == person
    assert token1.verification_type == VerificationToken.VERIFICATION_TYPE_CANCELLATION
    assert token1.email == person.email_address

    token2 = VerificationToken.objects.create_token(
        enrolment, person, VerificationToken.VERIFICATION_TYPE_CANCELLATION, email=email
    )
    assert token2.email == email


@pytest.mark.django_db
def test_verification_token_deactivate_and_create_token(
    mock_get_event_data,
):
    enrolment = EnrolmentFactory()
    person = enrolment.person
    token1 = VerificationToken.objects.create_token(
        enrolment, person, VerificationToken.VERIFICATION_TYPE_CANCELLATION
    )
    assert VerificationToken.objects.get(pk=token1.pk).is_active is True
    token2 = VerificationToken.objects.deactivate_and_create_token(
        enrolment, person, VerificationToken.VERIFICATION_TYPE_CANCELLATION
    )
    assert VerificationToken.objects.get(pk=token1.pk).is_active is False
    assert VerificationToken.objects.get(pk=token2.pk).is_active is True


@pytest.mark.django_db
def test_clean_invalid_tokens_defaults(mock_get_event_data):
    EnrolmentVerificationTokenFactory(is_active=True)
    EnrolmentVerificationTokenFactory(is_active=False)
    EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() - timedelta(minutes=10)
    )
    assert VerificationToken.objects.count() == 3
    VerificationToken.objects.clean_invalid_tokens()
    assert VerificationToken.objects.count() == 1


@pytest.mark.django_db
def test_clean_invalid_tokens_inactive(mock_get_event_data):
    EnrolmentVerificationTokenFactory(is_active=True)
    EnrolmentVerificationTokenFactory(is_active=False)
    expired_token = EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() - timedelta(minutes=10)
    )
    assert VerificationToken.objects.count() == 3
    VerificationToken.objects.clean_invalid_tokens(
        clean_inactive=True, clean_expired=False
    )
    assert VerificationToken.objects.count() == 2
    assert VerificationToken.objects.filter(pk=expired_token.pk).exists()


@pytest.mark.django_db
def test_clean_invalid_tokens_expired(mock_get_event_data):
    EnrolmentVerificationTokenFactory(is_active=True)
    inactive_token = EnrolmentVerificationTokenFactory(is_active=False)
    EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() - timedelta(minutes=10)
    )
    assert VerificationToken.objects.count() == 3
    VerificationToken.objects.clean_invalid_tokens(
        clean_inactive=False, clean_expired=True
    )
    assert VerificationToken.objects.count() == 2
    assert VerificationToken.objects.filter(pk=inactive_token.pk).exists()
