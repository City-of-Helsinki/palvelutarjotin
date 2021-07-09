from django.apps import AppConfig


class OrganisationsConfig(AppConfig):
    name = "organisations"

    def ready(self):
        import organisations.notifications  # noqa
