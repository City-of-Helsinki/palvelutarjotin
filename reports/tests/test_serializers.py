from reports.models import EnrolmentReport
from reports.serializers import EnrolmentReportSerializer


def test_enrolment_report_to_representation():
    report = EnrolmentReport(
        occurrence_languages=[["fi", "Finnish"]],
        study_group_study_levels=[["age_0_2", "age 0-2"]],
        keywords=[["kultus:5", "Musiikki"]],
        occurrence_place_position=[24.670147, 60.20042],
        study_group_unit_position=[24.862606, 60.251762],
    )
    serializer = EnrolmentReportSerializer(instance=report)
    assert serializer.data["study_group_study_levels"][0] == {
        "id": "age_0_2",
        "label": "age 0-2",
    }
    assert serializer.data["occurrence_languages"][0] == {"id": "fi", "name": "Finnish"}
    assert serializer.data["keywords"][0] == {"id": "kultus:5", "name": "Musiikki"}
    assert serializer.data["occurrence_place_position"] == {
        "longitude": 24.670147,
        "latitude": 60.20042,
    }
    assert serializer.data["study_group_unit_position"] == {
        "longitude": 24.862606,
        "latitude": 60.251762,
    }


def test_enrolment_report_to_internal():
    report_json = {
        "study_group_study_levels": [{"id": "age_0_2", "label": "age 0-2"}],
        "occurrence_languages": [{"id": "fi", "name": "Finnish"}],
        "keywords": [{"id": "kultus:5", "name": "Musiikki"}],
        # Rest are for is_valid -call
        "study_group_amount_of_children": 1,
        "study_group_amount_of_adult": 1,
        "enrolment_time": "2021-11-08T17:16:55.356724+02:00",
        "enrolment_status": "approved",
        "occurrence_place_id": "tprek:59265",
        "occurrence_cancelled": False,
        "occurrence_amount_of_seats": 10,
        "occurrence_start_time": "2021-11-14T00:00:00+02:00",
        "occurrence_end_time": "2021-11-14T01:00:00+02:00",
        "linked_event_id": "local-kultus:af6p5lyfxu",
        "enrolment_start_time": "2021-11-08T10:45:38.439000+02:00",
        "occurrence_place_position": {"longitude": 24.670147, "latitude": 60.20042},
        "study_group_unit_position": {"longitude": 24.862606, "latitude": 60.251762},
    }
    report = EnrolmentReportSerializer(data=report_json)
    report.is_valid()
    data = report.validated_data
    assert data["occurrence_languages"][0] == ["fi", "Finnish"]
    assert data["study_group_study_levels"][0] == ["age_0_2", "age 0-2"]
    assert data["keywords"][0] == ["kultus:5", "Musiikki"]
    assert data["occurrence_place_position"] == [24.670147, 60.20042]
    assert data["study_group_unit_position"] == [24.862606, 60.251762]
