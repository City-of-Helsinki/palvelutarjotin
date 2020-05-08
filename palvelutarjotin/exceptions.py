from graphql import GraphQLError


class PalvelutarjotinGraphQLError(GraphQLError):
    """GraphQLError that is not sent to Sentry."""


class DataValidationError(PalvelutarjotinGraphQLError):
    """Error in object validation"""


class ApiUsageError(PalvelutarjotinGraphQLError):
    """Wrong API usage"""


class ObjectDoesNotExistError(PalvelutarjotinGraphQLError):
    """Object does not exist"""


class QueryTooDeepError(PalvelutarjotinGraphQLError):
    """Query depth exceeded settings.PALVELUTARJOTIN_QUERY_MAX_DEPTH"""


class MissingDefaultTranslationError(PalvelutarjotinGraphQLError):
    """Missing default translation for translatable object"""


class IncorrectGlobalIdError(PalvelutarjotinGraphQLError):
    """Unexpected node type from global id"""
