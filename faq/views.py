from django.shortcuts import render

from .models import Faq


def display_faq(request):
    """ A view to show all the FAQs in display order, lowest first """

    faqs = Faq.objects.all().order_by('display')
    print(faqs)
    context = {
        'faqs': faqs,
    }

    return render(request, 'faq/faq.html', context)
