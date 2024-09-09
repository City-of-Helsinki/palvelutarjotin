from django.db import models

from gdpr.consts import CLEARED_VALUE


class GDPRModel(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # raise a NotImplementedError
        # immediately on launch of an app
        # if the `gdpr_sensitive_data_fields` is not defined.
        self.gdpr_sensitive_data_fields

    class Meta:
        abstract = True

    @property
    def gdpr_sensitive_data_fields(self) -> list[str]:
        raise NotImplementedError(
            "The model that is extending abstract GDPRModel class "
            "must define a `gdpr_sensitive_data_fields` -field "
            "with names of the GDPR sensitive fields."
        )

    def clear_gdpr_sensitive_data_fields(self):
        """Clears all the GDPR data fields set by
        the static ``get_gdpr_sensitive_data_fields`` property
        and then calls ``save()`` for the model instance.

        If the field is blankable, set an empty string as an value.
        Else if the field is nullable, set None as a value.
        Else, set a ``CLEARED_VALUE`` constant as a value.

        NOTE: This method should be overridden if
        anything else is needed or wanted.
        """
        for field in self.gdpr_sensitive_data_fields:
            if self._meta.get_field(field).blank:
                setattr(self, field, "")
            elif self._meta.get_field(field).null:
                setattr(self, field, None)
            else:
                setattr(self, field, CLEARED_VALUE)
        self.save()
