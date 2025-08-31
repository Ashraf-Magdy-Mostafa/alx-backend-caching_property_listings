import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger("properties.cache")

CACHE_KEY_ALL_PROPERTIES = "all_properties"

def get_all_properties():
    """Low-level caching of the Property queryset for 1 hour."""
    qs = cache.get(CACHE_KEY_ALL_PROPERTIES)
    if qs is None:
        qs = list(Property.objects.all())  # store as list to avoid querysets serialization gotchas
        cache.set(CACHE_KEY_ALL_PROPERTIES, qs, 3600)
        logger.info("Cached all properties (count=%s) for 3600s.", len(qs))
    else:
        logger.info("Returned properties from cache (count=%s).", len(qs))
    return qs

def get_redis_cache_metrics():
    """Return Redis keyspace hit/miss metrics and hit ratio."""
    conn = get_redis_connection("default")
    info = conn.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total else 0.0
    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": round(hit_ratio, 4),
    }
    logger.info("Redis metrics: %s", metrics)
    return metrics
