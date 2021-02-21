from django.contrib import admin
from products.models import ProductReviews


class ProductReviewAdmin(admin.ModelAdmin):

    list_display = (
        'date_created',
        'user',
        'rating',
        'product',
        'comment',
    )

    ordering = ('date_created',)


admin.site.register(ProductReviews, ProductReviewAdmin)
