from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
from .utils import CACHE_KEY_ALL_PROPERTIES
import logging

logger = logging.getLogger("properties.cache")

@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(CACHE_KEY_ALL_PROPERTIES)
    logger.info("Invalidated '%s' cache due to Property save (id=%s).", CACHE_KEY_ALL_PROPERTIES, instance.id)

@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(CACHE_KEY_ALL_PROPERTIES)
    logger.info("Invalidated '%s' cache due to Property delete (id=%s).", CACHE_KEY_ALL_PROPERTIES, instance.id)
