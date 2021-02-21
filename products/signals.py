from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProductReviews


@receiver(post_save, sender=ProductReviews)
def update_product_on_save(sender, instance, created, **kwargs):
    """
    Update the average rating on the product when review is created or updated
    """
    instance.product.update_average_rating()


@receiver(post_delete, sender=ProductReviews)
def update_product_on_delete(sender, instance, **kwargs):
    """
    Update the average rating on the product when review is deleted
    """
    instance.product.update_average_rating()
