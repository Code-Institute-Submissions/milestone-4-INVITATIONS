from django.contrib import admin
from .models import Product, CustomDetailLine, Category, ProductReviews


class CustomDetailLineAdminInline(admin.TabularInline):
    model = CustomDetailLine


class ProductReviewsAdminInline(admin.TabularInline):
    model = ProductReviews


class ProductAdmin(admin.ModelAdmin):
    inlines = (CustomDetailLineAdminInline, ProductReviewsAdminInline)

    readonly_fields = ('average_rating',)

    list_display = (
        'pk',
        'name',
        'category',
        'price',
        'featured',
        'date_created',
        'view_image',
    )

    ordering = ('date_created',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
