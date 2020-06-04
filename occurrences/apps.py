from django.apps import AppConfig


class OccurrencesConfig(AppConfig):
    name = "occurrences"

    def ready(self):
        import occurrences.notifications  # noqa
        import occurrences.signals  # noqa
