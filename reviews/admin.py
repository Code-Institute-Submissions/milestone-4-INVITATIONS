from django.contrib import admin
from products.models import ProductReviews


class ProductReviewAdmin(admin.ModelAdmin):
    """ Reviews layout for django admin """
    list_display = (
        'pk',
        'date_created',
        'user',
        'rating',
        'product',
        'comment',
    )

    ordering = ('-date_created',)


admin.site.register(ProductReviews, ProductReviewAdmin)
