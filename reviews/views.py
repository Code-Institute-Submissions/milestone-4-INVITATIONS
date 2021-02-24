from django.shortcuts import render, redirect

from .forms import ReviewForm
from products.models import Product

from django.contrib import messages


def reviews(request):
    """ A view add a new review """

    return render(request, 'reviews/reviews.html')


def add_review(request, product_id, order_id):
    """ A view add a new review """
    print('Reviewing product: ', product_id)

    if request.POST:
        form_data = {
            'comment': request.POST['comment'],
            'rating': request.POST['rating'],
            'product': product_id,
            'user': request.user.id,
        }

        form = ReviewForm(form_data)

        if form.is_valid():
            print('Form was valid')
            form.save()
            messages.success(request, 'Your review has been successfully \
                             added',
                             extra_tags='reviews')
            return redirect('home')

        else:
            print('Form FAILED')
            messages.error(request, 'Review submission failed,  please \
                           double-check your form and retry.',
                           extra_tags='reviews')

    else:
        # form = ReviewForm(initial={'product': product_id})
        form = ReviewForm()

    form.helper.form_action += f'/{product_id}/{order_id}/'

    product = Product.objects.get(pk=product_id)

    context = {
        'form': form,
        'product_name': product.name,
        'product_image': product.view_image,
    }
    return render(request, 'reviews/add_review.html', context)
