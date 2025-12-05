import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties with low-level caching.
    Caches the queryset in Redis for 1 hour.
    """
    # Check if properties are cached
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        logger.info("Properties retrieved from cache")
        return cached_properties
    
    # If not cached, fetch from database
    logger.info("Properties not found in cache, fetching from database")
    properties = list(Property.objects.all())
    
    # Cache the queryset for 1 hour (3600 seconds)
    cache.set('all_properties', properties, 3600)
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with hit ratio and other metrics.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO statistics
        info = redis_conn.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2),
            'connected_clients': info.get('connected_clients', 0),
            'used_memory': info.get('used_memory', 0),
            'used_memory_human': info.get('used_memory_human', '0B'),
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
        }
