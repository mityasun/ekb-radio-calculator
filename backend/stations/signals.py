from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from stations.models import RadioStation
from utils.utils import clear_cache


@receiver(post_save, sender=RadioStation)
@receiver(post_delete, sender=RadioStation)
def clear_stations_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*",
    ]
    clear_cache(patterns)
