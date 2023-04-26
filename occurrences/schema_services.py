import requests
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from typing import List, Optional, Tuple, Union

from common.utils import (
    get_node_id_from_global_id,
    get_obj_from_global_id,
    update_object,
)
from occurrences.models import (
    Enrolment,
    EventQueueEnrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
)
from organisations.models import Person
from palvelutarjotin.exceptions import (
    CaptchaValidationFailedError,
    DataValidationError,
    EnrolCancelledOccurrenceError,
    EnrolmentClosedError,
    EnrolmentMaxNeededOccurrenceReached,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    InvalidStudyGroupSizeError,
    InvalidStudyGroupUnitInfoError,
    InvalidTokenError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
)
from verification_token.models import VerificationToken


def validate_occurrence_data(p_event, kwargs, updated_obj=None):
    end_time = (
        kwargs.get("end_time", updated_obj.end_time)
        if updated_obj
        else kwargs["end_time"]
    )
    start_time = (
        kwargs.get("start_time", updated_obj.start_time)
        if updated_obj
        else kwargs["start_time"]
    )
    if end_time <= start_time:
        raise DataValidationError("End time must be after start time")
    minimum_time = (
        (p_event.enrolment_start + timedelta(days=p_event.enrolment_end_days))
        if p_event.enrolment_end_days
        else p_event.enrolment_start
    )
    if minimum_time is not None and start_time < minimum_time:
        raise DataValidationError("Start time cannot be before the enrolment ends")


@transaction.atomic
def add_contact_persons_to_object(info, contact_persons, obj):
    obj.contact_persons.clear()
    for p in contact_persons:
        p_global_id = p.get("id", None)
        if p_global_id:
            person = get_obj_from_global_id(info, p_global_id, Person)
        else:
            person = Person.objects.create(**p)
        obj.contact_persons.add(person)


def validate_study_group(study_group: Union[StudyGroup, dict]):
    if not isinstance(study_group, dict):
        study_group_data = study_group.__dict__
    else:
        study_group_data = dict(study_group)
    if not study_group_data.get("unit_id") and not study_group_data.get("unit_name"):
        raise InvalidStudyGroupUnitInfoError(
            "Study group should always have an unit id or an unit name."
        )


def validate_enrolment(  # noqa: C901
    study_group: StudyGroup, occurrence: Occurrence, new_enrolment=True
):
    validate_study_group(study_group)

    # Expensive validation are sorted to bottom
    if (
        occurrence.p_event.mandatory_additional_information
        and not study_group.extra_needs
    ):
        raise MissingMantatoryInformationError(
            "This event requires additional information of study group"
        )
    if occurrence.cancelled:
        raise EnrolCancelledOccurrenceError("Cannot enrol cancelled occurrence")
    if study_group.group_size_with_adults() < 1:
        raise InvalidStudyGroupSizeError(
            "Study group should contain at least 1 participant"
        )
    elif (
        occurrence.max_group_size
        and study_group.group_size_with_adults() > occurrence.max_group_size
    ) or (
        occurrence.min_group_size
        and study_group.group_size_with_adults() < occurrence.min_group_size
    ):
        raise InvalidStudyGroupSizeError(
            "Study group size not match occurrence group size"
        )
    if not occurrence.p_event.enrolment_start or (
        timezone.now() < occurrence.p_event.enrolment_start
    ):
        raise EnrolmentNotStartedError("Enrolment is not opened")
    if timezone.now() > occurrence.start_time - timedelta(
        days=occurrence.p_event.enrolment_end_days
    ):
        raise EnrolmentClosedError("Enrolment has been closed")
    # Skip these validations when updating enrolment
    if new_enrolment:
        if (
            study_group.occurrences.filter(
                p_event=occurrence.p_event, cancelled=False
            ).count()
            >= occurrence.p_event.needed_occurrences
        ):
            raise EnrolmentMaxNeededOccurrenceReached(
                "Number of enrolled occurrences is greater than the needed occurrences"
            )
        if (
            occurrence.seats_taken
            + (
                study_group.group_size_with_adults()
                if occurrence.seat_type
                == Occurrence.OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT
                else 1
            )
        ) > occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )
    else:
        if occurrence.seats_taken > occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )


def verify_captcha(key):
    if not key:
        raise CaptchaValidationFailedError("Missing captcha verification data")
    secret_key = settings.RECAPTCHA_SECRET_KEY
    verify_url = settings.RECAPTCHA_VALIDATION_URL

    # captcha verification
    data = {"response": key, "secret": secret_key}
    resp = requests.post(verify_url, data=data, timeout=5)
    result_json = resp.json()

    if result_json.get("success"):
        return True
    else:
        raise CaptchaValidationFailedError(
            f"Captcha verification failed: {result_json.get('error-codes')}"
        )


def verify_enrolment_token(enrolment, token):
    try:
        token_obj = VerificationToken.objects.get(key=token)
    except VerificationToken.DoesNotExist:
        raise InvalidTokenError("Token is invalid or expired")
    if token_obj.content_object != enrolment or not token_obj.is_valid():
        raise InvalidTokenError("Token is invalid or expired")


def create_study_group(study_group_data):
    study_levels_data = study_group_data.pop("study_levels")

    person_data = study_group_data.pop("person")
    person = get_or_create_contact_person(person_data)
    study_group_data["person_id"] = person.id
    validate_study_group(study_group_data)
    study_group = StudyGroup.objects.create(**study_group_data)
    study_group.study_levels.set(
        get_instance_list(StudyLevel, map(lambda x: x.lower(), study_levels_data))
    )

    return study_group


def update_study_group(study_group_data, study_group_obj=None):
    if not study_group_obj:
        study_group_global_id = study_group_data.pop("id")
        study_group_id = get_node_id_from_global_id(
            study_group_global_id, "StudyGroupNode"
        )
        try:
            study_group_obj = StudyGroup.objects.get(id=study_group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

    # Handle a person
    person_data = study_group_data.pop("person", None)
    if person_data:
        person = get_or_create_contact_person(person_data)
        study_group_data["person_id"] = person.id

    # Handle study levels
    study_levels_data = study_group_data.pop("study_levels", None)
    if study_levels_data:
        study_group_obj.study_levels.set(
            get_instance_list(StudyLevel, map(lambda x: x.lower(), study_levels_data))
        )

    validate_study_group(study_group_data)

    # update the populated object
    update_object(study_group_obj, study_group_data)
    return study_group_obj


def get_or_create_contact_person(contact_person_data):
    """
    If a contact person id is given,
    get a contact person with a given non-assignable id
    or else, create a contact person with a given data.
    """
    if contact_person_data.get("id"):
        person_id = get_node_id_from_global_id(
            contact_person_data.get("id"), "PersonNode"
        )
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
    else:
        person = Person.objects.create(**contact_person_data)
    return person


def get_instance_list(ModelClass, instance_pks: List[str]):
    result = []
    for instance_pk in instance_pks:
        try:
            instance = ModelClass.objects.get(pk=instance_pk)
            result.append(instance)
        except ModelClass.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
    return result


def enrol_to_occurrence(
    study_group: StudyGroup,
    occurrences: List[Occurrence],
    person: Person,
    notification_type,
    send_notifications=True,
):
    enrolments: List[Enrolment] = []
    notifiable_enrolments: List[Tuple[Enrolment, Optional[str]]] = []

    for occurrence in occurrences:
        validate_enrolment(study_group, occurrence)
        enrolment: Enrolment = Enrolment.objects.create(
            study_group=study_group,
            occurrence=occurrence,
            person=person,
            notification_type=notification_type,
        )

        if occurrence.p_event.auto_acceptance:
            custom_message: Optional[
                str
            ] = enrolment.occurrence.p_event.safe_translation_getter(
                "auto_acceptance_message", language_code=person.language
            )
            enrolment.approve(send_notification=False)
            notifiable_enrolments.append((enrolment, custom_message))

        enrolments.append(enrolment)

    if send_notifications:
        for enrolment, custom_message in notifiable_enrolments:
            enrolment.send_approve_notification(custom_message=custom_message)

    return enrolments


def enrol_to_event_queue(
    study_group: StudyGroup,
    p_event: PalvelutarjotinEvent,
    person: Person,
    notification_type,
):
    validate_study_group(study_group)
    try:
        event_queue_enrolment = EventQueueEnrolment.objects.get(
            p_event=p_event, study_group__group_name=study_group.group_name
        )
    except EventQueueEnrolment.DoesNotExist:
        event_queue_enrolment = EventQueueEnrolment(
            p_event=p_event,
            study_group=study_group,
            person=person,
            notification_type=notification_type,
        )
    return event_queue_enrolment
