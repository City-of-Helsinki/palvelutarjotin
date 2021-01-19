from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from occurrences.models import Enrolment
from verification_token.factories import EnrolmentVerificationTokenFactory
from verification_token.models import VerificationToken

User = get_user_model()


@pytest.mark.django_db
def test_enrolment_verification_token_creation():
    verification_token = EnrolmentVerificationTokenFactory()
    assert VerificationToken.objects.count() == 1
    assert verification_token.content_object.__class__ == Enrolment
    assert verification_token.key is not None


@pytest.mark.django_db
def test_verification_token_is_valid():
    valid_token = EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() + timedelta(days=1)
    )
    invalid_token1 = EnrolmentVerificationTokenFactory(
        expiry_date=timezone.now() - timedelta(days=1)
    )
    invalid_token2 = EnrolmentVerificationTokenFactory(is_active=False)
    assert valid_token.is_valid() is True
    assert invalid_token1.is_valid() is False
    assert invalid_token2.is_valid() is False
