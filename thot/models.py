from django.db import models


class TimestampsMixin(models.Model):
    """
    Abstract model for TimestampsMixin
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        """
        Meta class for TimestampsMixin
        """

        abstract = True

    @property
    def is_deleted(self):
        """
        Method that checks if deleted_at is not None.
        """
        return self.deleted_at is not None
