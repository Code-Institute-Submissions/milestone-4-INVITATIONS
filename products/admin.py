from django.contrib import admin
from .models import Product, CustomDetailLine, Category


class CustomDetailLineAdminInline(admin.TabularInline):
    model = CustomDetailLine


class ProductAdmin(admin.ModelAdmin):
    inlines = (CustomDetailLineAdminInline,)

    list_display = (
        'pk',
        'name',
        'category',
        'price',
        'featured',
        'date_created',
        'raw_image',
    )

    ordering = ('date_created',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
