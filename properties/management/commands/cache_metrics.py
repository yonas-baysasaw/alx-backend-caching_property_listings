from django.core.management.base import BaseCommand
from properties.utils import get_redis_cache_metrics


class Command(BaseCommand):
    help = 'Display Redis cache metrics'

    def handle(self, *args, **options):
        metrics = get_redis_cache_metrics()
        
        self.stdout.write(self.style.SUCCESS('Redis Cache Metrics:'))
        self.stdout.write(f"Keyspace Hits: {metrics['keyspace_hits']}")
        self.stdout.write(f"Keyspace Misses: {metrics['keyspace_misses']}")
        self.stdout.write(f"Total Requests: {metrics['total_requests']}")
        self.stdout.write(f"Hit Ratio: {metrics['hit_ratio']}%")
        self.stdout.write(f"Connected Clients: {metrics['connected_clients']}")
        self.stdout.write(f"Used Memory: {metrics['used_memory_human']}")
        
        if 'error' in metrics:
            self.stdout.write(
                self.style.ERROR(f"Error: {metrics['error']}")
            )
