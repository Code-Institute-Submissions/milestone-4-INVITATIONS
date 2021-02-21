from django.shortcuts import render


def reviews(request):
    """ A view to show your reviews """

    return render(request, 'reviews/reviews.html')
