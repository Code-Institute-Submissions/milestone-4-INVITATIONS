from django.contrib import admin
from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
        'display',
    )

    ordering = ('display',)


admin.site.register(Faq, FaqAdmin)
