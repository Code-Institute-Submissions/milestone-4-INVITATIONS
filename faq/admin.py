from django.contrib import admin
from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    """ Admin layout details for faqs """

    list_display = (
        'question',
        'answer',
        'display',
    )

    ordering = ('display',)


admin.site.register(Faq, FaqAdmin)
