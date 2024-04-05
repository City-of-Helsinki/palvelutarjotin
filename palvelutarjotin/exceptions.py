from graphql import GraphQLError


class PalvelutarjotinEventHasNoOccurrencesError(Exception):
    """Event has no occurrences when it should"""


class PalvelutarjotinGraphQLError(GraphQLError):
    """GraphQLError that is not sent to Sentry."""


class DataValidationError(PalvelutarjotinGraphQLError):
    """Error in object validation"""


class ApiUsageError(PalvelutarjotinGraphQLError):
    """Wrong API usage"""


class ObjectDoesNotExistError(PalvelutarjotinGraphQLError):
    """Object does not exist"""


class ApiBadRequestError(PalvelutarjotinGraphQLError):
    """Bad request, e.g. JsonDecodeError"""


class QueryTooDeepError(PalvelutarjotinGraphQLError):
    """Query depth exceeded settings.PALVELUTARJOTIN_QUERY_MAX_DEPTH"""


class MissingDefaultTranslationError(PalvelutarjotinGraphQLError):
    """Missing default translation for translatable object"""


class IncorrectGlobalIdError(PalvelutarjotinGraphQLError):
    """Unexpected node type from global id"""


class AlreadyJoinedEventError(PalvelutarjotinGraphQLError):
    """Study group already enrol in the event"""


class EnrolmentMaxNeededOccurrenceReached(PalvelutarjotinGraphQLError):
    """Number of enroled occurrences greater than needed occurrences"""


class EnrolmentNotStartedError(PalvelutarjotinGraphQLError):
    """Occurrence is not opened for enrolment"""


class EnrolmentNotEnoughCapacityError(PalvelutarjotinGraphQLError):
    """Not enough space for the study group"""


class EnrolmentClosedError(PalvelutarjotinGraphQLError):
    """Enrolment period closed"""


class InvalidStudyGroupSizeError(PalvelutarjotinGraphQLError):
    """Study group size greater than required max group size or smaller than min group
    size"""


class InvalidStudyGroupUnitInfoError(PalvelutarjotinGraphQLError):
    """Study group should always have an unit id or an unit name."""


class InvalidEmailFormatError(PalvelutarjotinGraphQLError):
    """Invalid email format error"""


class EnrolCancelledOccurrenceError(PalvelutarjotinGraphQLError):
    """Enrol cancelled occurrence"""


class CaptchaValidationFailedError(PalvelutarjotinGraphQLError):
    """Captcha validation failed"""


class UploadImageSizeExceededError(PalvelutarjotinGraphQLError):
    """Uploaded image size larger than settings.MAX_UPLOAD_SIZE"""


class MissingMantatoryInformationError(PalvelutarjotinGraphQLError):
    """When pEvent.mantatory_additional_information is True,
    study_group.extra_needs is required in the mutation"""


class InvalidTokenError(PalvelutarjotinGraphQLError):
    """Invalid verification token or token expired"""


class QueueingNotAllowedError(PalvelutarjotinGraphQLError):
    """Queueing is not allowed for the event"""
