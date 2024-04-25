from django.db import models


class DefaultOneMixin(models.Model):
    """
    A mixin class to ensure only one instance in the model has default=True.
    """

    default = models.BooleanField('По умолчанию', default=False)

    def save(self, *args, **kwargs):
        if self.default:
            self.__class__.objects.exclude(pk=self.pk).update(default=False)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
