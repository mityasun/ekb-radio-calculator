from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def created_superuser_is_active(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.is_active = True
        instance.save()
