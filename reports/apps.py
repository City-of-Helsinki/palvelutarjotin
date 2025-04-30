from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = "reports"

    def ready(self):
        import reports.schema_extensions  # noqa: F401
