from typing import List

from reports.models import EnrolmentReport
from rest_framework import serializers


class Size2ArrayField(serializers.Field):
    def __init__(self, first_value_name: str = "id", second_value_name: str = "label"):
        self.first_value_name = first_value_name
        self.second_value_name = second_value_name
        super().__init__()

    def _array_to_dict(self, entry: List[str]):
        if len(entry) != 2:
            raise ValueError(
                "Size2ArrayField field value should always "
                "have a length of 2 (id, interpretation)."
            )
        return {self.first_value_name: entry[0], self.second_value_name: entry[1]}

    def _dict_to_array(self, entry: dict):
        return [entry[self.first_value_name], entry[self.second_value_name]]

    def to_representation(self, value):
        return [self._array_to_dict(entry) for entry in value] if value else None

    def to_internal_value(self, data):
        return [self._dict_to_array(entry) for entry in data] if data else None


class EnrolmentReportSerializer(serializers.ModelSerializer):
    study_group_study_levels = Size2ArrayField(
        first_value_name="id", second_value_name="label"
    )
    occurrence_languages = Size2ArrayField(
        first_value_name="id", second_value_name="name"
    )
    keywords = Size2ArrayField(first_value_name="id", second_value_name="name")

    class Meta:
        model = EnrolmentReport
        fields = "__all__"
