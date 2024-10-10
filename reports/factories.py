import factory

from occurrences.factories import EnrolmentFactory
from reports.models import EnrolmentReport


class EnrolmentReportFactory(factory.django.DjangoModelFactory):
    enrolment = factory.SubFactory(EnrolmentFactory)

    class Meta:
        model = EnrolmentReport
        skip_postgeneration_save = True  # Not needed after factory v4.0.0
