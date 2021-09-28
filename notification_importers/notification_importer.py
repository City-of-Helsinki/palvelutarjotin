import csv
import glob
import io
import os
import re
from collections import defaultdict
from logging import getLogger
from typing import DefaultDict, Dict, Mapping, Optional, Sequence, Tuple

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.models import NotificationTemplate, NotificationTemplateException
from django_ilmoitin.utils import render_notification_template
from parler.utils.context import switch_language
from requests import RequestException

# {
#     "<notification type>": {
#         "<language code>": {
#             "<field name>": "<field value>",
#             ...
#         },
#         ...
#     },
#     ...
# }
SourceData = Mapping[str, Mapping[str, Mapping[str, str]]]


logger = getLogger(__name__)


class NotificationImporterException(Exception):
    pass


class AbstractNotificationImporter:
    """
    An abstract base class for Notification Importer classes.
    Original source:
    https://github.com/City-of-Helsinki/kukkuu/blob/master/importers/notification_importer.py
    1. Some function and variable renaming done.
    2. Splitted code from original importer to create an abstract class
    """

    LANGUAGES = settings.PARLER_SUPPORTED_LANGUAGE_CODES
    FIELDS = ("subject", "body_text", "body_html")

    @transaction.atomic()
    def create_missing_and_update_existing_notifications(self) -> Tuple[int, int]:
        num_of_created = self.create_missing_notifications()
        num_of_updated = self.update_notifications(NotificationTemplate.objects.all())
        return num_of_created, num_of_updated

    @transaction.atomic()
    def create_missing_notifications(self) -> int:
        new_types = set(self.source_data.keys()) - set(
            NotificationTemplate.objects.values_list("type", flat=True)
        )
        for new_type in sorted(new_types):
            new_notification = NotificationTemplate(type=new_type)
            self._create_or_update_notification_using_source_data(new_notification)

        return len(new_types)

    @transaction.atomic()
    def update_notifications(
        self, notifications: Sequence[NotificationTemplate]
    ) -> int:
        num_of_updated = 0

        for notification in sorted(notifications, key=lambda n: n.type):
            if self.is_notification_in_sync(notification) is False:
                self._create_or_update_notification_using_source_data(notification)
                num_of_updated += 1

        return num_of_updated

    def is_notification_in_sync(
        self, notification: NotificationTemplate
    ) -> Optional[bool]:
        if notification.type not in self.source_data:
            return None

        for language in self.LANGUAGES:
            try:
                translation_obj = notification.translations.get(language_code=language)
            except ObjectDoesNotExist:
                translation_obj = None

            for field in self.FIELDS:
                current_value = (
                    self.clean_text(getattr(translation_obj, field))
                    if translation_obj
                    else ""
                )
                source_value = self._get_value_from_source(
                    notification.type, field, language
                )

                if current_value != source_value:
                    return False

        return True

    def _get_value_from_source(
        self, notification_type: str, field: str, language: str
    ) -> str:
        return (
            self.source_data.get(notification_type, {}).get(language, {}).get(field, "")
        )

    def _create_or_update_notification_using_source_data(
        self, notification: NotificationTemplate
    ):
        creating = not bool(notification.pk)

        for language in self.LANGUAGES:
            with switch_language(notification, language):
                for field in self.FIELDS:
                    setattr(
                        notification,
                        field,
                        self._get_value_from_source(notification.type, field, language),
                    )
                notification.save()

            # Test that the notification can be rendered without errors.
            # This create/update method is called inside a transaction so the
            # notification will not get actually saved in case of an error.
            try:
                render_notification_template(
                    notification,
                    context=dummy_context.get(notification.type),
                    language_code=language,
                )
            except NotificationTemplateException as e:
                raise NotificationImporterException(
                    f'Error rendering notification "{notification}": {e}'
                ) from e

        logger.info(
            f'{"Created" if creating else "Updated"} notification "{notification}"'
        )

    def _fetch_data(self) -> SourceData:
        raise NotImplementedError

    @staticmethod
    def clean_text(text: str) -> str:
        return text.replace("\u202f", " ").replace("\r\n", "\n")


class NotificationGoogleSheetImporter(AbstractNotificationImporter):
    """
    Imports NotificationTemplates from Google Sheets.
    Original source:
    https://github.com/City-of-Helsinki/kukkuu/blob/master/importers/notification_importer.py
    1. Some function and variable renaming done.
    2. Splitted code from original importer to create an abstract class
    """

    TIMEOUT = 5
    HEADER_FIELD_AND_LANGUAGE_SEPARATOR = "|"

    def __init__(self, sheet_id: str = None) -> None:
        self.sheet_id = (
            sheet_id or settings.NOTIFICATIONS_SHEET_ID
            if hasattr(settings, "NOTIFICATIONS_SHEET_ID")
            else None
        )
        if not self.sheet_id:
            raise NotificationImporterException("Sheet ID not set.")

        self.source_data: SourceData = self._fetch_data()

    @property
    def url(self) -> str:
        return (
            f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"
        )

    def _fetch_data(self) -> SourceData:
        csv_data = self.__fetch_csv_data()
        return self.__get_source_data_from_csv_file(io.StringIO(csv_data))

    def __get_field_and_language_from_header(self, header: str) -> Tuple[str, str]:
        field, language = header.split(self.HEADER_FIELD_AND_LANGUAGE_SEPARATOR)
        return field.lower().strip(), language.lower().strip()

    def __fetch_csv_data(self) -> str:
        try:
            response = requests.get(self.url, timeout=self.TIMEOUT)
            response.raise_for_status()
        except RequestException as e:
            raise NotificationImporterException(
                f"Error fetching data from the spreadsheet: {e}"
            ) from e
        return response.content.decode("utf-8")

    def __get_source_data_from_csv_file(self, csv_file: io.StringIO) -> SourceData:
        reader = csv.DictReader(csv_file)
        source_data = {}

        for row in reader:
            notification_data: DefaultDict[str, Dict[str, str]] = defaultdict(dict)

            row_items = iter(row.items())
            # the first column contains notification type
            notification_type = next(row_items)[1].lower()

            for header, content in row_items:
                field, language = self.__get_field_and_language_from_header(header)
                notification_data[language][field] = self.clean_text(content)

            source_data[notification_type] = notification_data

        return source_data


class NotificationFileImporter(AbstractNotificationImporter):
    """
    Import notification templates from template files.
    The templates files should be stored in notification_importers app in
    notification_importers/templates/sms and notification_importers/templates/email
    folders. There is also a naming convention used there.
    The file name must be given in this pattern [notification_type]-[locale].[html|j2].
    """

    def __init__(self) -> None:
        self.template_dirs = ["/templates/email", "/templates/sms"]
        self.files = sorted(
            [
                filename
                for template_dir in self.template_dirs
                for ext in ("*.html", "*.j2")
                for filename in glob.iglob(
                    os.path.dirname(os.path.abspath(__file__))
                    + template_dir
                    + f"**/{ext}",
                    recursive=True,
                )
            ]
        )
        self.source_data: SourceData = self._fetch_data()

    def _fetch_data(self) -> SourceData:
        source_data: SourceData = defaultdict(lambda: defaultdict(dict))
        for template_file_path in self.files:
            with open(template_file_path, "r") as template_file:
                pathname = os.path.splitext(template_file.name)[0]
                filename = pathname.split("/")[-1]
                notification_type, language = filename.split("-")
                field = (
                    "body_text"
                    if self.__is_sms_template(template_file)
                    else "body_html"
                )
                content = template_file.read()
                source_data[notification_type][language][field] = self.clean_text(
                    content
                )
                source_data[notification_type][language][
                    "subject"
                ] = self.__get_subject(content, notification_type)

        return source_data

    def __get_subject(
        self, file_content: io.TextIOWrapper, notification_type: str
    ) -> str:
        """
        Returns a title element content from a HTML file as a notification subject.
        If a title cannot be found, it uses the file name as a subject.
        """
        title_rgx = re.compile(r"\<title\>(\S.*)\<\/title\>")
        subject = (
            title_rgx.search(file_content).group(1)
            if title_rgx.search(file_content)
            else notification_type.__str__().replace("_", " ")
        )
        return subject

    def __is_sms_template(self, template_file: io.TextIOWrapper) -> bool:
        return True if "sms" in template_file.name else False
