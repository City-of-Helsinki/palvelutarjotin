from typing import List, Optional

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import serializers

from reports.models import EnrolmentReport


class NamedPairField(serializers.Field):
    def __init__(self, first_value_name: str = "id", second_value_name: str = "label"):
        self.first_value_name = first_value_name
        self.second_value_name = second_value_name
        super().__init__()

    def _array_to_dict(self, entry: List[str]):
        if len(entry) != 2:
            raise ValueError(
                "NamedPairField field value should always "
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
        if not isinstance(data, dict):
            raise serializers.ValidationError(
                "Expected a dictionary containing longitude and latitude."
            )
        longitude = data.get("longitude")
        latitude = data.get("latitude")

        if longitude is None or latitude is None:
            raise serializers.ValidationError(
                "Both longitude and latitude are required."
            )

        try:
            longitude = float(longitude)
            latitude = float(latitude)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Longitude and latitude must be numeric values."
            )

        return [longitude, latitude]


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
                    (
                        self.translations[key] if key in self.translations else key
                    ): value.capitalize()
                    for (key, value) in pairs
                },
            }
            # Countries are uppercased in ISO-format
            result["country"] = result["country"].upper()
            return result
        return None

    def to_internal_value(self, data: dict) -> list:
        """
        A detailed dict represented in a JSON view back to original OCD ids list format

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
            ]"""

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


class BaseMappedBooleanField(serializers.Field):
    """
    Bidirectional serializer for a BooleanField with translatable labels for
    False and True values.
    """

    @property
    def false_label(self) -> str:
        raise NotImplementedError("Subclasses must define a false_label property.")

    @property
    def true_label(self) -> str:
        raise NotImplementedError("Subclasses must define a true_label property.")

    def to_representation(self, value) -> str:
        return self.true_label if value else self.false_label

    def to_internal_value(self, data) -> bool:
        # This is likely worst case 6 ifs (fi/sv/en languages and two labels):
        for lang_code, _lang_name in settings.LANGUAGES:
            with translation.override(lang_code):
                if data == self.false_label:
                    return False
                if data == self.true_label:
                    return True
        raise serializers.ValidationError(f"Unable to parse {data} as a boolean.")


class IsPartOfCulturalRouteField(BaseMappedBooleanField):
    @property
    def false_label(self) -> str:
        # Django has fi/sv/en translations for "No" and "Unknown" out of the box:
        return f"{_('No')} / {_('Unknown')}"

    @property
    def true_label(self) -> str:
        # Django has fi/sv/en translations for "Yes" out of the box:
        return _("Yes")


class EnrolmentReportSerializer(serializers.ModelSerializer):
    occurrence_place_position = PositionField()
    study_group_unit_position = PositionField()
    study_group_unit_divisions = OCDIDField()
    occurrence_place_divisions = OCDIDField()
    study_group_study_levels = NamedPairField(
        first_value_name="id", second_value_name="label"
    )
    occurrence_languages = NamedPairField(
        first_value_name="id", second_value_name="name"
    )
    keywords = NamedPairField(first_value_name="id", second_value_name="name")
    is_part_of_cultural_route = IsPartOfCulturalRouteField()

    class Meta:
        model = EnrolmentReport
        fields = "__all__"
