# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product
from .cach_keys import POPULAR_PRODUCTS_KEY_CACHE_KEY

@receiver(post_save, sender=Product)
def clear_cache_on_product_save(sender, instance, created, **kwargs):
    """ Clear cache when a product is added or updated """
    cache.delete(POPULAR_PRODUCTS_KEY_CACHE_KEY)  # Use the cache key defined in your viewset
    print("Cache cleared due to product save")

@receiver(post_delete, sender=Product)
def clear_cache_on_product_delete(sender, instance, **kwargs):
    """ Clear cache when a product is deleted """
    cache.delete(POPULAR_PRODUCTS_KEY_CACHE_KEY)  # Use the cache key defined in your viewset
    print("Cache cleared due to product delete")
