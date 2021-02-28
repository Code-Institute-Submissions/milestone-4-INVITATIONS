from django.shortcuts import render


def index(request):
    """ Index / home page view """

    return render(request, 'home/index.html')


def our_story(request):
    """ Our Story page view """

    return render(request, 'home/our_story.html')


def terms_conditions(request):
    """ Terms and Conditions page view """

    return render(request, 'home/terms.html')


def privacy_policy(request):
    """ Privacy Policy page view """

    return render(request, 'home/privacy.html')


def delivery_info(request):
    """ Delivery Information page view """

    return render(request, 'home/delivery.html')


def contact_us(request):
    """ Contact Us page view """

    return render(request, 'home/contact.html')
