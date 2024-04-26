from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from rates.models import BlockPosition
from settings.models import SystemText, City, AudioDuration, TimeInterval, \
    AudienceAge, AudienceSex, Month
from utils.utils import clear_cache


@receiver(post_save, sender=SystemText)
@receiver(post_delete, sender=SystemText)
def clear_system_texts_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.system-texts:*.GET.*",
    ]
    clear_cache(patterns)


@receiver(post_save, sender=City)
@receiver(post_delete, sender=City)
def clear_cities_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.cities:*.GET.*",
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=Month)
@receiver(post_delete, sender=Month)
def clear_month_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=AudioDuration)
@receiver(post_delete, sender=AudioDuration)
def clear_audio_durations_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.audio-durations:*.GET.*",
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=BlockPosition)
@receiver(post_delete, sender=BlockPosition)
def clear_block_positions_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.block-positions:*.GET.*",
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=TimeInterval)
@receiver(post_delete, sender=TimeInterval)
def clear_time_intervals_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.time-intervals:*.GET.*",
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=AudienceSex)
@receiver(post_delete, sender=AudienceSex)
def clear_audience_sex_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)


@receiver(post_save, sender=AudienceAge)
@receiver(post_delete, sender=AudienceAge)
def clear_audience_age_cache(sender, instance, **kwargs):

    patterns = [
        "*:views.decorators.cache.cache_page.radiostations:*.GET.*"
    ]
    clear_cache(patterns)
