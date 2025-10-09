import logging
from typing import TYPE_CHECKING, Optional

from helsinki_gdpr.types import ErrorResponse

if TYPE_CHECKING:
    from organisations.models import User as UserType

logger = logging.getLogger(__name__)


def get_user(user: "UserType") -> "UserType":
    """Function used by the Helsinki Profile GDPR API to get the "user"
    instance from the "GDPR Model"
    instance. Since in our case the GDPR Model
    and the user are one and the same, we simply return
    the same User instance that is given as a parameter.

    Args:
        user (UserType): the User instance whose GDPR data is being queried

    Returns:
        UserType: the same User instance

    References:
        https://github.com/City-of-Helsinki/kukkuu/blob/e5b12aae778db6270d57de67bc0dd3d5870efa28/gdpr/service.py
        https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/blob/808dcd30a745f6d18cdf36ccaf07b0cd25844ab0/README.md.
        https://github.com/City-of-Helsinki/kerrokantasi/blob/256134d4049f0bd1598d59caaebbb813be2d7d9c/kerrokantasi/gdpr.py.
    """
    logger.info(f"GDPR data request called for user '{user.uuid}'.")
    return user


def delete_data(user: "UserType", dry_run: bool) -> Optional[ErrorResponse]:
    logger.info(f"GDPR data delete called for user '{user.uuid}'.")
    user.delete()
