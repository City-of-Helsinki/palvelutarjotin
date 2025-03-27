from django.db import connection
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable


class DatabaseHealthCheck(BaseHealthCheckBackend):
    """
    Custom health check for the database connection.
    """

    critical_service = True

    def check_status(self):
        """
        Checks the database connection by executing a simple query.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM organisations_user LIMIT 1")
        except Exception as e:
            raise ServiceUnavailable(f"Database connection failed: {e}")

    def identifier(self):
        return self.__class__.__name__  # Display name on the endpoint.
