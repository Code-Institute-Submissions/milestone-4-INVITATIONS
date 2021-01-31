from django.shortcuts import render, redirect, reverse, get_object_or_404

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
            products = Product.objects.order_by('-date_created')[:2]
            main_title = 'new products'

        elif 'search-text' in request.GET:
            search_text = request.GET['search-text']
            if not search_text:
                return redirect(reverse('products'))

            products = Product.objects.all().filter(
                name__icontains=search_text).order_by(default_sort)

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

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)
