from django.shortcuts import render


def index(request):
    """ Index / ome page view """

    return render(request, 'home/index.html')
