from django.shortcuts import render
from django.http import HttpResponse

from .models import Faq


def zdisplay_faq(request):
    """ A view to show all the FAQs in display order, lowest first """

    faqs = Faq.objects.all().order_by('display')
    print(faqs)
    context = {
        'faqs': faqs,
    }

    return render(request, 'faq/faq.html', context)


def display_faq(request):
    # Return an "Internal Server Error" 500 response code.
    return HttpResponse(status=500)
