from django.shortcuts import render, redirect

from .forms import ReviewForm
from products.models import Product, ProductReviews

from django.contrib import messages


def reviews(request):
    """ A view add a new review """

    return render(request, 'reviews/reviews.html')


def add_review(request, product_id, order_id):
    """ A view to add a new review """
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
        form = ReviewForm(is_add=True)

    form.helper.form_action += f'add/{product_id}/{order_id}/'

    product = Product.objects.get(pk=product_id)

    context = {
        'form': form,
        'product_name': product.name,
        'product_image': product.view_image,
    }
    return render(request, 'reviews/add_review.html', context)


def edit_review(request, review_id):
    """ A view to edit an existing review """
    print('Editing review: ', review_id)

    review = ProductReviews.objects.get(pk=int(review_id))
    product = Product.objects.get(pk=review.product.pk)

    if request.POST:
        form_data = {
            'pk': review_id,
            'comment': request.POST['comment'],
            'rating': request.POST['rating'],
            'product': product.pk,
            'user': request.user.id,
        }

        form = ReviewForm(form_data)

        if form.is_valid():
            print('Form was valid')
            do_update = ProductReviews.objects.filter(
                id=int(review_id)).update(
                    comment=request.POST['comment'],
                    rating=int(request.POST['rating']))
            print('Update: ', do_update)
            # form.save()
            messages.success(request, 'Your review has been successfully \
                             updated',
                             extra_tags='reviews')
            return redirect('user_profile')

        else:
            print('Form FAILED')
            messages.error(request, 'Review edit failed,  please \
                           double-check your form and retry.',
                           extra_tags='reviews')

    else:
        form = ReviewForm(instance=review)

    form.helper.form_action += f'edit/{review_id}/'

    # print('Layout', list(form.helper.layout))
    # print('Layout', form.helper.layout[3])
    # print('Layout', form.helper.layout[3].html)
    # print('Layout', type(form.helper.layout[3]))

    context = {
        'form': form,
        'product_name': product.name,
        'product_image': product.view_image,
    }
    return render(request, 'reviews/add_review.html', context)
