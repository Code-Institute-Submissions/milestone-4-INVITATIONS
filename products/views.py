from django.shortcuts import render

from .models import Product, Category


def products(request):
    """ A view to show all the products """

    default_sort = 'date_created'
    main_title = 'all products'
    categories = None
    show = None
    if 'show' in request.GET:
        show = request.GET['show']

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            print(len(categories))
            products = Product.objects.filter(
                category__name__in=categories).order_by(
                    'category', default_sort)
            # categories = list(Category.objects.filter(name__in=categories))
            categories = Category.objects.filter(name__in=categories)
            if len(categories) == 1:
                # main_title = "single name"
                # main_title = [category.display_name for category in categories]
                for category in categories:
                    main_title = category.display_name
                    print(main_title)
            else:
                main_title = show
            # print(type(categories))
            # for category in categories:
            #     print(category.display_name)

        elif show == 'featured':
            products = Product.objects.filter(
                featured=True).order_by('category', default_sort)
            main_title = 'featured products'

        elif show == 'new':
            products = Product.objects.order_by('-date_created')[:2]
            main_title = 'new products'

    else:
        products = Product.objects.all().order_by(default_sort)

    context = {
        'products': products,
        'main_title': main_title,
        'categories': categories,
    }

    return render(request, 'products/products.html', context)
