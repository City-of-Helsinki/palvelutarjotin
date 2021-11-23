import factory
from occurrences.factories import EnrolmentFactory
from reports.models import EnrolmentReport


class EnrolmentReportFactory(factory.django.DjangoModelFactory):

    enrolment = factory.SubFactory(EnrolmentFactory)

    class Meta:
        model = EnrolmentReport
