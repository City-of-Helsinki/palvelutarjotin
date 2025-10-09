import csv
import logging
from functools import lru_cache

from auditlog.context import set_actor
from auditlog.signals import accessed
from django.conf import settings
from django.http.response import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission

from common.utils import (
    get_client_ip,
)
from occurrences.models import PalvelutarjotinEvent
from organisations.models import Organisation, Person
from palvelutarjotin.oidc import KultusApiTokenAuthentication
from reports.models import EnrolmentReport
from reports.serializers import EnrolmentReportSerializer
from reports.services import get_place_json_from_linkedevents
from reports.views.mixins import (
    ExportReportViewMixin,
    OrganisationPersonsMixin,
    PalvelutarjotinEventEnrolmentsMixin,
    PersonsMixin,
)

logger = logging.getLogger(__name__)


class IsEventAdminUser(BasePermission):
    """
    Allows access only to event admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_event_staff)


class ExportReportCsvView(ExportReportViewMixin, generics.GenericAPIView):
    """
    A generic API view that provides functionality to export model data as a CSV file.

    This view is designed to be subclassed by specific report views that need to
    export data in CSV format. It handles authentication, permissions, CSV response
    creation, and writing data from a queryset based on the specified `model`.

    Subclasses must define the `model` attribute to indicate which Django model
    should be queried for the report data. The CSV file will include all fields
    of the model as columns.
    """

    model = None
    serializer_class = None
    authentication_classes = [KultusApiTokenAuthentication, SessionAuthentication]
    permission_classes = [IsEventAdminUser]
    csv_dialect = csv.excel
    csv_delimiter = ";"

    def _create_csv_response_writer(self, filename):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(filename)

        """
        Adding BOM is not advicable, and UTF-8 shouldn't even have that,
        but Microsoft product seems to sometimes need it.
        """
        response.write("\ufeff")

        """
        CSV is a delimited text file that uses a comma to separate values
        (many implementations of CSV import/export tools allow other
        separators to be used; for example, the use of a "Sep=^" row
        as the first row in the csv file will cause Excel to open
        the file expecting caret "^" to be the separator instead of comma ",").
        ~ https://en.wikipedia.org/wiki/Comma-separated_values.
        NOTE: At least when using a comma as a delimiter,
        the separator is needed to be defined for Microsoft Excel.
        NOTE: When tested with Microsoft Excel for Mac, strangely,
        it seems to help Excel to choose the delimiter, but seems to break encoding
        and the scandinavian letters are not shown properly.
        """
        # response.write(f"sep={self.csv_delimiter}{self.csv_dialect.lineterminator}")

        """
        The CSV library uses Excel as the default dialect,
        but Excel still seems not to work properly with it,
        since there were issues with the separator and the encoding.
        Using the semicolon (";") as a delimiter
        seems to fix UTF-8 issues with Microsoft Excel.
        """
        writer = csv.writer(
            response, dialect=self.csv_dialect, delimiter=self.csv_delimiter
        )

        return writer, response

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        writer, response = self._create_csv_response_writer(meta)
        writer.writerow(field_names)
        with set_actor(actor=request.user, remote_addr=get_client_ip(request)):
            for obj in queryset:
                accessed.send(sender=obj.__class__, instance=obj)
                writer.writerow([getattr(obj, field) for field in field_names])

        return response


class PersonsCsvView(PersonsMixin, ExportReportCsvView):
    """
    API endpoint that exports a CSV file listing all persons.
    """

    model = Person

    @extend_schema(
        operation_id="exportPersonsCsv",
        summary=_("Export a CSV of all persons."),
        description=_(
            "Exports a CSV file where each row represents a person and includes "
            "their name, email address, phone number, and a comma-separated list "
            "of the organisations they are associated with."
        ),
        responses={
            ("200", "text/csv"): OpenApiResponse(
                response=OpenApiTypes.STR,
                description=_("A CSV file containing data for all persons."),
                examples=[
                    OpenApiExample(
                        "CSV Persons Data",
                        "Name,Email,Phone,Organisations\n"
                        "John Doe,john.doe@example.com,0123456789,Helsinki City Library,Org2\n"  # noqa: E501
                        "Jane Smith,jane.smith@example.com,0987654321,Helsinki Culture Centre\n"  # noqa: E501
                        "Peter Jones,peter.jones@example.com,1122334455,",  # noqa: E501
                        media_type="text/csv",
                        summary=_("Example CSV output showing all persons"),
                    ),
                ],
            ),
        },
        tags=["Reports CSV export"],
    )
    def get(self, request, *args, **kwargs):
        writer, response = self._create_csv_response_writer("kultus_persons")
        writer.writerow([_("Name"), _("Email"), _("Phone"), _("Organisations")])
        with set_actor(actor=request.user, remote_addr=get_client_ip(request)):
            for person in self.get_queryset().order_by("name"):
                # write access logs to auditlog
                accessed.send(sender=person.__class__, instance=person)
                writer.writerow(
                    [
                        person.name,
                        person.email_address,
                        person.phone_number,
                        ", ".join([o.name for o in person.organisations.all()]),
                    ]
                )
        return response


class OrganisationPersonsCsvView(OrganisationPersonsMixin, ExportReportCsvView):
    """
    API endpoint that exports a CSV file listing persons associated with each
    organisation.
    """

    model = Organisation

    @extend_schema(
        operation_id="exportOrganisationPersonsCsv",
        summary=_("Export a CSV of persons associated with each organisation."),
        description=_(
            "Exports a CSV file where each row represents a person and includes "
            "the name of the organisation they are associated with, along with "
            "the person's name, email, and phone number."
        ),
        responses={
            ("200", "text/csv"): OpenApiResponse(
                response=OpenApiTypes.STR,
                description=_(
                    "A CSV file containing a list of organisations and their "
                    "associated persons."
                ),
                examples=[
                    OpenApiExample(
                        "CSV Organisation Persons Data",
                        "Organisation,Name,Email,Phone\n"
                        "Helsinki City Library,John Doe,john.doe@example.com,0123456789\n"  # noqa: E501
                        "Helsinki City Library,Jane Smith,jane.smith@example.com,0987654321\n"  # noqa: E501
                        "Helsinki Culture Centre,Peter Jones,peter.jones@example.com,1122334455",  # noqa: E501
                        media_type="text/csv",
                        summary=_(
                            "Example CSV output showing organisations and persons"
                        ),
                    ),
                ],
            ),
        },
        tags=["Reports CSV export"],
    )
    def get(self, request, *args, **kwargs):
        writer, response = self._create_csv_response_writer(
            "kultus_organisations_persons"
        )
        writer.writerow([_("Organisation"), _("Name"), _("Email"), _("Phone")])

        with set_actor(actor=request.user, remote_addr=get_client_ip(request)):
            for organisation in self.get_queryset():
                for person in organisation.persons.all().order_by("name"):
                    # write access logs to auditlog
                    accessed.send(sender=person.__class__, instance=person)
                    writer.writerow(
                        [
                            organisation.name,
                            person.name,
                            person.email_address,
                            person.phone_number,
                        ]
                    )
        return response


class PalvelutarjotinEventEnrolmentsCsvView(
    PalvelutarjotinEventEnrolmentsMixin, ExportReportCsvView
):
    """
    API endpoint that exports a CSV file listing enrolments for Palvelutarjotin events.
    """

    model = PalvelutarjotinEvent

    DATE_FORMAT = "%d.%m.%y"
    TIME_FORMAT = "%H:%M:%S"

    # fetch every place_id only once
    @staticmethod
    @lru_cache()
    def _get_place_from_linkedevents_or_cache(place_id):
        return get_place_json_from_linkedevents(place_id)

    def _write_csv_header_row(self, writer):
        writer.writerow(
            [
                _("Enrolment id"),
                _("LinkedEvents id"),
                _("LinkedEvents uri"),
                _("Event starting date"),
                _("Event starting time"),
                _("Event ending date"),
                _("Event ending time"),
                _("Enrolment date"),
                _("Enrolment time"),
                _("Kindergarten / school / college"),
                _("Group name"),
                _("Study levels"),
                _("Amount of children"),
                _("Amount of adults"),
                _("Event location"),
                _("Extra needs"),
                _("Contact mail"),
                _("Contact phone"),
            ]
        )

    def _write_csv_data_row(self, writer, enrolment):
        start_datetime = timezone.localtime(enrolment.occurrence.start_time)
        end_datetime = timezone.localtime(enrolment.occurrence.end_time)
        enrolment_datetime = timezone.localtime(enrolment.enrolment_time)

        place = (
            self._get_place_from_linkedevents_or_cache(enrolment.occurrence.place_id)
            if enrolment.occurrence.place_id
            else None
        )

        if enrolment.person:
            person_email_address = enrolment.person.email_address
            person_phone_number = enrolment.person.phone_number
        elif enrolment.person_deleted_at:
            person_email_address = person_phone_number = (
                f"{_('Deleted')} "
                + f"{enrolment.person_deleted_at.strftime(self.DATE_FORMAT)}"
            )
        else:
            person_email_address = person_phone_number = ""

        writer.writerow(
            [
                enrolment.id,
                enrolment.occurrence.p_event.linked_event_id,
                "{linked_events_root}event/{linked_event_id}".format(
                    linked_events_root=settings.LINKED_EVENTS_API_CONFIG["ROOT"],
                    linked_event_id=enrolment.occurrence.p_event.linked_event_id,
                ),
                start_datetime.strftime(self.DATE_FORMAT),
                start_datetime.strftime(self.TIME_FORMAT),
                end_datetime.strftime(self.DATE_FORMAT),
                end_datetime.strftime(self.TIME_FORMAT),
                enrolment_datetime.strftime(self.DATE_FORMAT),
                enrolment_datetime.strftime(self.TIME_FORMAT),
                enrolment.study_group.unit_name,
                enrolment.study_group.group_name,
                ", ".join(
                    [
                        study_level.label
                        for study_level in enrolment.study_group.study_levels.all()
                    ]
                ),
                enrolment.study_group.group_size,
                enrolment.study_group.amount_of_adult,
                (
                    place["name"].get("fi")
                    or place["name"].get("sv")
                    or place["name"].get("en")
                )
                if place
                else "",
                enrolment.study_group.extra_needs,
                person_email_address,
                person_phone_number,
            ]
        )

    def _write_csv_events_approved_enrolments_table(self, request):
        writer, response = self._create_csv_response_writer(
            "kultus_events_approved_enrolments"
        )
        # write access logs to auditlog
        with set_actor(
            actor=request.user,
            remote_addr=get_client_ip(request),
        ):
            self._write_csv_header_row(writer)
            for enrolment in self.get_queryset():
                accessed.send(sender=enrolment.__class__, instance=enrolment)
                self._write_csv_data_row(writer, enrolment)

        return response

    @extend_schema(
        operation_id="exportPalvelutarjotinEventEnrolmentsCsv",
        summary=_("Export Palvelutarjotin event enrolments CSV"),
        description=_(
            "Exports a CSV file containing a list of enrolments for events. "
            "Each row represents an enrolment and includes details such as "
            "the enrolment ID, linked event information, event dates and times, "
            "enrolment date and time, study group details, location, contact "
            "information, and extra needs."
        ),
        responses={
            ("200", "text/csv"): OpenApiResponse(
                response=OpenApiTypes.STR,
                description=_(
                    "A CSV file containing Palvelutarjotin event enrolment data."
                ),
                examples=[
                    OpenApiExample(
                        "CSV Event Enrolments Data",
                        "Enrolment id,LinkedEvents id,LinkedEvents uri,Event starting date,Event starting time,Event ending date,Event ending time,Enrolment date,Enrolment time,Kindergarten / school / college,Group name,Study levels,Amount of children,Amount of adults,Event location,Extra needs,Contact mail,Contact phone\n"  # noqa: E501
                        "123,linked-event-1,https://api.hel.fi/linkedevents/v1/event/linked-event-1,2025-05-10,10:00:00,2025-05-10,12:00:00,2025-05-01,14:30:00,Example School,Group A,preschool,15,2,Example Location,,contact@example.com,0123456789",  # noqa: E501
                        media_type="text/csv",
                        summary=_("Example CSV output showing event enrolments"),
                    ),
                ],
            ),
        },
        tags=["Reports CSV export"],
    )
    def get(self, request, *args, **kwargs):
        # Inform the user if not all the data was included
        self.message_max_result(request)
        return self._write_csv_events_approved_enrolments_table(request)


class EnrolmentReportCsvView(ExportReportCsvView):
    """
    API endpoint that exports a CSV file containing enrolment reports.

    This view inherits from `ExportReportCsvView` and uses the `EnrolmentReport`
    model to generate the CSV data. The CSV file will contain all fields
    defined in the `EnrolmentReport` model.
    """

    model = EnrolmentReport
    serializer_class = EnrolmentReportSerializer

    @extend_schema(
        operation_id="exportEnrolmentReportsCsv",
        summary=_("Export enrolment reports CSV"),
        description=_("Exports a CSV file containing a list of all enrolment reports."),
        responses={
            ("200", "text/csv"): OpenApiResponse(
                response=OpenApiTypes.STR,
                description=_("A CSV file containing enrolment report data."),
                examples=[
                    OpenApiExample(
                        "CSV Enrolment Reports Data",
                        "id,occurrence_place_position,study_group_unit_position,study_group_unit_divisions,occurrence_place_divisions,study_group_study_levels,occurrence_languages,keywords,created_at,updated_at,study_group_unit_id,study_group_amount_of_children,study_group_amount_of_adult,enrolment_time,enrolment_status,occurrence_place_id,occurrence_cancelled,occurrence_amount_of_seats,occurrence_start_time,occurrence_end_time,linked_event_id,enrolment_start_time,enrolment_externally,provider,publisher,distance_from_unit_to_event_place,_study_group,_enrolment,_occurrence\n"  # noqa: E501
                        '1,"{\\"longitude\\": 24.945831, \\"latitude\\": 60.192059}","{\\"longitude\\": 24.945831, \\"latitude\\": 60.192059}","{\\"ocd_ids\\": [\\"ocd-division/country:fi/kunta:helsinki\\"], \\"country\\": \\"FI\\", \\"municipality\\": \\"Helsinki\\"}","{\\"ocd_ids\\": [\\"ocd-division/country:fi/kunta:helsinki\\"], \\"country\\": \\"FI\\", \\"municipality\\": \\"Helsinki\\"}",[{"id": "preschool", "label": "Preschool"}],[],[],2025-04-30T10:00:00Z,2025-04-30T10:00:00Z,unit-1,10,2,2025-05-05T12:00:00Z,approved,place-1,False,20,2025-05-10T10:00:00Z,2025-05-10T12:00:00Z,linked-event-1,2025-05-01T09:00:00Z,False,provider-a,publisher-b,1.5,1,1,1',  # noqa: E501
                        media_type="text/csv",
                        summary=_("Example CSV output of enrolment reports"),
                    ),
                ],
            ),
        },
        tags=["Reports CSV export"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
