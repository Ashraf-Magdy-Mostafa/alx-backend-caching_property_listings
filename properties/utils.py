import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger("properties.cache")


def get_all_properties():
    qs = cache.get("all_properties")
    if qs is None:
        qs = list(Property.objects.all())
        cache.set("all_properties", qs, 3600)
        logger.info("Cached all properties (count=%s) for 3600s.", len(qs))
    else:
        logger.info("Returned properties from cache (count=%s).", len(qs))
    return qs


def get_redis_cache_metrics():
    try:
        conn = get_redis_connection("default")
        info = conn.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }
        logger.info("Redis metrics: %s", metrics)
        return metrics
    except Exception as e:
        logger.error("Failed to fetch Redis metrics: %s", e)
        return {"error": str(e)}
