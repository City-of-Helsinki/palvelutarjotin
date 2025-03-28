from auditlog.context import set_actor
from auditlog.signals import accessed
from rest_framework import mixins


class LogListAccessMixin(mixins.ListModelMixin):
    """
    Mixin to log access to each object in a list view queryset, specifically
    handling paginated results.

    This mixin extends `ListModelMixin` to log access events for each object
    retrieved in a list view, taking pagination into account. It overrides
    `paginate_queryset` to ensure that access logs are written for the
    objects on the current page.

    Example Usage:

    ```python
    from rest_framework import generics
    from .models import MyModel
    from .serializers import MyModelSerializer


    class MyModelListView(LogListAccessMixin, generics.ListAPIView):
        queryset = MyModel.objects.all()
        serializer_class = MyModelSerializer
    ```

    Attributes:
        accessed (Signal): A Django signal that is sent for each accessed object.

    Methods:
        paginate_queryset(self, queryset):
            Overrides the `paginate_queryset` method to log access events for
            objects on the current page.
        _write_audit_access_log_of_paginated_objects(self, queryset):
            Writes access log to audit log of each instance in the provided queryset.

    Returns:
        QuerySet: The paginated queryset retrieved by the parent's
                    `paginate_queryset` method, or the original queryset if
                    pagination is disabled.
    """

    def _write_audit_access_log_of_paginated_objects(self, queryset):
        """
        Writes access log to audit log of each instance in the paginated queryset.

        This private method iterates through the provided queryset and sends
        the `accessed` signal for each object, logging the access event.

        Args:
            queryset: The paginated queryset (or the original queryset if
                        pagination is disabled) to log access events for.
        """
        user = self.request.user
        with set_actor(user):
            for obj in queryset:
                accessed.send(sender=obj.__class__, instance=obj)

    def paginate_queryset(self, queryset):
        """
        Paginates the queryset and logs access for each object on the current page.

        This method overrides the default `paginate_queryset` method to first
        paginate the queryset and then log access events for each object in the
        resulting page (or the original queryset if pagination is disabled).

        Args:
            queryset: The queryset to paginate.

        Returns:
            QuerySet: The paginated queryset, or the original queryset if
                        pagination is disabled.
        """
        page = super().paginate_queryset(queryset)

        logged_objects = page if page is not None else queryset
        self._write_audit_access_log_of_paginated_objects(logged_objects)

        return page


class SaveAfterPostGenerationMixin:
    """
    Mixin for saving Django model instances after post-generation hooks.

    To use this derive the factory class that uses @factory.post_generation
    decorator from factory.django.DjangoModelFactory as well as this, e.g.
    class TestFactory(SaveAfterPostGenerationMixin, factory.django.DjangoModelFactory)

    NOTE: Needs to be before factory.django.DjangoModelFactory in the class
    definition to work, because of how Python resolves method resolution order (MRO).

    Rationale:
     - Because factory 3.3.0 has deprecated saving the instance after
       post-generation hooks, and will remove the functionality in the
       next major release.
    """

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()
