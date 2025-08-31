from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger("properties.cache")


@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete('all_properties')
    logger.info(
        "Invalidated 'all_properties' cache due to Property save (id=%s).", instance.id)


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_properties')
    logger.info(
        "Invalidated 'all_properties' cache due to Property delete (id=%s).", instance.id)
