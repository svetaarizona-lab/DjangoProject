from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book


@receiver(post_save, sender=Book)
def clear_book_cache_on_save(sender, instance, **kwargs):
    cache.delete(f"book_{instance.pk}")
    cache.delete("views.decorators.cache.cache_page..GET....")
    cache.clear()


@receiver(post_delete, sender=Book)
def clear_book_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f"book_{instance.pk}")
    cache.clear()