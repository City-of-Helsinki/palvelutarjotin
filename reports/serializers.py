from rest_framework import serializers
from typing import List, Optional

from reports.models import EnrolmentReport


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


class PositionField(serializers.Field):
    def to_representation(self, value):
        if value:
            return {"longitude": value[0], "latitude": value[1]}
        return None

    def to_internal_value(self, data):
        return [data["longitude"], data["latitude"]]


class OCDIDField(serializers.Field):
    """A serializer for Open Civic Data ID"""

    translations = {
        "peruspiiri": "district",
        "osa-alue": "sub_district",
        "kaupunginosa": "neighborhood",
        "kunta": "municipality",
    }

    def to_representation(self, value: list) -> Optional[dict]:
        """OCD id paths to a more detailed dict

        Args:
            value (list): A list of OCD ids, e.g.
            ```
            [
                "ocd-division/country:fi/kunta:helsinki/osa-alue:keski-pasila",
                "ocd-division/country:fi/kunta:helsinki/kaupunginosa:pasila",
                "ocd-division/country:fi/kunta:helsinki/peruspiiri:pasila",
                "ocd-division/country:fi/kunta:helsinki",
            ]
            ```

        Returns:
            dict: the original OCD ids list in the key "ocd-ids" and
            all the key-value -pairs of OCD id path, e.g.
            ```
            "ocd_ids": [
                "ocd-division/country:fi/kunta:helsinki/osa-alue:keski-pasila",
                "ocd-division/country:fi/kunta:helsinki/kaupunginosa:pasila",
                "ocd-division/country:fi/kunta:helsinki/peruspiiri:pasila",
                "ocd-division/country:fi/kunta:helsinki",
            ],
            "country": "FI",
            "municipality": "Helsinki",
            "sub_district": "Keski-pasila",
            "neighborhood": "Pasila",
            "district": "Pasila",
            ```
        """
        if value:
            joined = "/".join(value).replace("ocd-division/", "")
            pairs = [tuple(pair.split(":")) for pair in set(joined.split("/"))]
            result = {
                "ocd_ids": value,
                **{
                    self.translations[key]
                    if key in self.translations
                    else key: value.capitalize()
                    for (key, value) in pairs
                },
            }
            # Countries are uppercased in ISO-format
            result["country"] = result["country"].upper()
            return result
        return None

    def to_internal_value(self, data: dict) -> list:
        """A detailed dict represented in a JSON view back to original OCD ids list format

        Args:
            data (dict): the original OCD ids list in the key "ocd-ids" and
            all the key-value -pairs of OCD id path, e.g.
            ```
            "ocd_ids": [
                "ocd-division/country:fi/kunta:helsinki/osa-alue:keski-pasila",
                "ocd-division/country:fi/kunta:helsinki/kaupunginosa:pasila",
                "ocd-division/country:fi/kunta:helsinki/peruspiiri:pasila",
                "ocd-division/country:fi/kunta:helsinki",
            ],
            "country": "FI",
            "municipality": "Helsinki",
            "sub_district": "Keski-pasila",
            "neighborhood": "Pasila",
            "district": "Pasila",
            ```

        Returns:
            list: A list of OCD ids, e.g.
            ```
            [
                "ocd-division/country:fi/kunta:helsinki/osa-alue:keski-pasila",
                "ocd-division/country:fi/kunta:helsinki/kaupunginosa:pasila",
                "ocd-division/country:fi/kunta:helsinki/peruspiiri:pasila",
                "ocd-division/country:fi/kunta:helsinki",
            ]
        """  # noqa
        if "ocd_ids" in data:
            return data["ocd_ids"]

        country_and_city = (
            f"ocd-division/country:{data.pop('country').lower()}"
            f"/municipality:{data.pop('municipality').lower()}"
        )
        return [
            country_and_city,
            *[
                f"{country_and_city}/{key}:{value.lower()}"
                for (key, value) in data.items()
            ],
        ]


class EnrolmentReportSerializer(serializers.ModelSerializer):
    occurrence_place_position = PositionField()
    study_group_unit_position = PositionField()
    study_group_unit_divisions = OCDIDField()
    occurrence_place_divisions = OCDIDField()
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
