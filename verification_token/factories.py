import factory.django
import pytz
from django.contrib.contenttypes.models import ContentType

from occurrences.factories import EnrolmentFactory
from organisations.factories import PersonFactory

from .models import VerificationToken


class VerificationTokenFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    person = factory.SubFactory(PersonFactory)
    key = VerificationToken.generate_key()
    expiry_date = factory.Faker(
        "future_datetime", end_date="+15m", tzinfo=pytz.timezone("Europe/Helsinki")
    )
    is_active = True

    class Meta:
        exclude = ["content_object"]
        abstract = True
        skip_postgeneration_save = True  # Not needed after factory v4.0.0


class EnrolmentVerificationTokenFactory(VerificationTokenFactory):
    content_object = factory.SubFactory(EnrolmentFactory)
    verification_type = factory.Faker(
        "random_element",
        elements=[t[0] for t in VerificationToken.VERIFICATION_TOKEN_TYPE_CHOICES],
    )

    class Meta:
        model = VerificationToken
        skip_postgeneration_save = True  # Not needed after factory v4.0.0
