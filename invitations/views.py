from django.shortcuts import render


def custom_error_view(request):
    """ View for custom 500 page """

    return render(request, '500.html')
