from django.shortcuts import render

from .models import Product, Category


def products(request):
    """ A view to show all the products """

    products = Product.objects.all().order_by('date_created')
    print(products)
    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
