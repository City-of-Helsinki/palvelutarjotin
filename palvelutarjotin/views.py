import sentry_sdk
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from graphene_file_upload.django import FileUploadGraphQLView
from graphql_jwt.exceptions import PermissionDenied as JwtPermissionDenied

from palvelutarjotin.consts import (
    ALREADY_JOINED_EVENT_ERROR,
    API_USAGE_ERROR,
    CAPTCHA_VALIDATION_FAILED_ERROR,
    DATA_VALIDATION_ERROR,
    ENROL_CANCELLED_OCCURRENCE_ERROR,
    ENROLMENT_CLOSED_ERROR,
    ENROLMENT_NOT_STARTED_ERROR,
    GENERAL_ERROR,
    INCORRECT_GLOBAL_ID_ERROR,
    INVALID_EMAIL_FORMAT_ERROR,
    INVALID_STUDY_GROUP_SIZE_ERROR,
    INVALID_STUDY_GROUP_UNIT_INFO_ERROR,
    INVALID_TOKEN_ERROR,
    MAX_NEEDED_OCCURRENCES_REACHED_ERROR,
    MISSING_DEFAULT_TRANSLATION_ERROR,
    MISSING_MANDATORY_INFORMATION_ERROR,
    NOT_ENOUGH_CAPACITY_ERROR,
    OBJECT_DOES_NOT_EXIST_ERROR,
    PERMISSION_DENIED_ERROR,
    QUERY_TOO_DEEP_ERROR,
    QUEUEING_NOT_ALLOWED_ERROR,
    UPLOAD_IMAGE_SIZE_EXCEEDED_ERROR,
)
from palvelutarjotin.exceptions import (
    AlreadyJoinedEventError,
    ApiUsageError,
    CaptchaValidationFailedError,
    DataValidationError,
    EnrolCancelledOccurrenceError,
    EnrolmentClosedError,
    EnrolmentMaxNeededOccurrenceReached,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    IncorrectGlobalIdError,
    InvalidEmailFormatError,
    InvalidStudyGroupSizeError,
    InvalidStudyGroupUnitInfoError,
    InvalidTokenError,
    MissingDefaultTranslationError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
    PalvelutarjotinGraphQLError,
    QueryTooDeepError,
    QueueingNotAllowedError,
    UploadImageSizeExceededError,
)

error_codes_shared = {
    Exception: GENERAL_ERROR,
    ObjectDoesNotExistError: OBJECT_DOES_NOT_EXIST_ERROR,
    JwtPermissionDenied: PERMISSION_DENIED_ERROR,
    PermissionDenied: PERMISSION_DENIED_ERROR,
    ApiUsageError: API_USAGE_ERROR,
    DataValidationError: DATA_VALIDATION_ERROR,
    QueryTooDeepError: QUERY_TOO_DEEP_ERROR,
    IncorrectGlobalIdError: INCORRECT_GLOBAL_ID_ERROR,
}

error_codes_palvelutarjotin = {
    MissingDefaultTranslationError: MISSING_DEFAULT_TRANSLATION_ERROR,
    AlreadyJoinedEventError: ALREADY_JOINED_EVENT_ERROR,
    EnrolmentNotEnoughCapacityError: NOT_ENOUGH_CAPACITY_ERROR,
    EnrolmentNotStartedError: ENROLMENT_NOT_STARTED_ERROR,
    EnrolmentClosedError: ENROLMENT_CLOSED_ERROR,
    EnrolCancelledOccurrenceError: ENROL_CANCELLED_OCCURRENCE_ERROR,
    EnrolmentMaxNeededOccurrenceReached: MAX_NEEDED_OCCURRENCES_REACHED_ERROR,
    InvalidStudyGroupSizeError: INVALID_STUDY_GROUP_SIZE_ERROR,
    InvalidEmailFormatError: INVALID_EMAIL_FORMAT_ERROR,
    CaptchaValidationFailedError: CAPTCHA_VALIDATION_FAILED_ERROR,
    UploadImageSizeExceededError: UPLOAD_IMAGE_SIZE_EXCEEDED_ERROR,
    MissingMantatoryInformationError: MISSING_MANDATORY_INFORMATION_ERROR,
    InvalidTokenError: INVALID_TOKEN_ERROR,
    InvalidStudyGroupUnitInfoError: INVALID_STUDY_GROUP_UNIT_INFO_ERROR,
    QueueingNotAllowedError: QUEUEING_NOT_ALLOWED_ERROR,
}

sentry_ignored_errors = (
    ObjectDoesNotExist,
    JwtPermissionDenied,
    PermissionDenied,
)

error_codes = {**error_codes_shared, **error_codes_palvelutarjotin}


class SentryGraphQLView(FileUploadGraphQLView):
    def execute_graphql_request(self, request, data, query, *args, **kwargs):
        """Extract any exceptions and send some of them to Sentry"""
        result = super().execute_graphql_request(request, data, query, *args, **kwargs)
        # If 'invalid' is set, it's a bad request
        if result and result.errors and not result.invalid:
            errors = [
                e
                for e in result.errors
                if not isinstance(
                    getattr(e, "original_error", None), PalvelutarjotinGraphQLError
                )
            ]
            if errors:
                self._capture_sentry_exceptions(result.errors, query)
        return result

    def _capture_sentry_exceptions(self, errors, query):
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("graphql_query", query)
            for error in errors:
                if hasattr(error, "original_error"):
                    error = error.original_error
                sentry_sdk.capture_exception(error)

    @staticmethod
    def format_error(error):
        def get_error_code(exception):
            """Get the most specific error code for the exception via superclass"""
            for exception in exception.mro():
                try:
                    return error_codes[exception]
                except KeyError:
                    continue

        try:
            error_code = get_error_code(error.original_error.__class__)
        except AttributeError:
            error_code = GENERAL_ERROR
        formatted_error = super(SentryGraphQLView, SentryGraphQLView).format_error(
            error
        )
        if error_code and (
            isinstance(formatted_error, dict)
            and not (
                "extensions" in formatted_error
                and "code" in formatted_error["extensions"]
            )
        ):
            formatted_error["extensions"] = {"code": error_code}
        return formatted_error
