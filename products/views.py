from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.contrib import messages

from .models import Product, Category


def products(request):
    """ A view to show all the products """

    default_sort = 'date_created'
    main_title = 'all products'
    categories = None
    show = None
    search_text = None

    if 'show' in request.GET:
        show = request.GET['show']

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = Product.objects.filter(
                category__name__in=categories).order_by(
                    'category', default_sort)
            categories = Category.objects.filter(name__in=categories)

            if len(categories) == 1:
                main_title = categories[0].display_name
            else:
                main_title = show

            if main_title == 'invitations':
                for cat in categories:
                    cat.display_name = cat.display_name.rpartition(' ')[0]

        elif show == 'featured':
            products = Product.objects.filter(
                featured=True).order_by('category', default_sort)
            main_title = 'featured products'

        elif show == 'new':
            products = Product.objects.order_by('-date_created')[:4]
            main_title = 'new products'

        elif 'search-text' in request.GET:
            search_text = request.GET['search-text']
            if not search_text:
                return redirect(reverse('products'))

            text_query = Q(
                name__icontains=search_text) | Q(
                    description__icontains=search_text)

            products = Product.objects.all().filter(
                text_query).order_by(default_sort)

    else:
        products = Product.objects.all().order_by(default_sort)

    context = {
        'products': products,
        'main_title': main_title,
        'search_text': search_text,
        'categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show a products information """

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        messages.error(request,
                       'Sorry that product cannot be found',
                       extra_tags='product error')

        return redirect('products')

    else:
        context = {
                'product': product,
        }

        if product.customizable:
            custom_lines = product.customlines.all()
            context['custom_lines'] = custom_lines

        return render(request, 'products/product_info.html', context)
