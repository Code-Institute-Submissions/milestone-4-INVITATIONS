from django.shortcuts import render, redirect

from .forms import ReviewForm
from products.models import Product, ProductReviews
from checkout.models import Order, OrderLineItem

from django.contrib import messages


def reviews(request):
    """ A view add a new review """

    return render(request, 'reviews/reviews.html')


def add_review(request, product_id, order_id):
    """ A view to add a new review """
    print('Reviewing product: ', product_id)

    try:
        order_lines = OrderLineItem.objects.get(order=int(order_id),
                                                product=int(product_id))
    except OrderLineItem.DoesNotExist:
        messages.error(request, 'Cannot locate order containing that product.',
                       extra_tags='reviews')
        return redirect('user_profile')

    print('Order: ', order_lines)
    ordered_by = order_lines.order
    # print('User', ordered_by.first_name)

    if request.user != ordered_by.user:
        messages.error(request, 'Order not found in your order history with that product line.',
                         extra_tags='reviews')
        return redirect('user_profile')

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
    """ A view to edit/delete reviews reviews """
    print('Editing review: ', review_id)

    try:
        review = ProductReviews.objects.get(pk=int(review_id))
    except ProductReviews.DoesNotExist:
        messages.error(request, 'Review has not been found.',
                         extra_tags='reviews')
        return redirect('user_profile')

    if request.user != review.user:
        messages.error(request, 'Review not found in your profile',
                         extra_tags='reviews')
        return redirect('user_profile')

    product = Product.objects.get(pk=review.product.pk)

    if request.POST:
        try:
            delete_or_not = int(request.POST['delete-review'])
            print(f'Delete checkbox is set to: {delete_or_not}')
        except KeyError:
            print('Delete box NOT checked')
            delete_or_not = 0

        form_data = {
            'pk': review_id,
            'comment': request.POST['comment'],
            'rating': request.POST['rating'],
            'product': product.pk,
            'user': request.user.id,
        }

        form = ReviewForm(form_data, instance=review)

        if form.is_valid():
            print('Form was valid')

            if delete_or_not == 1:
                print('Delete box IS checked')
                review.delete()
                messages.success(request, 'Your review has been deleted',
                                 extra_tags='reviews')
                return redirect('user_profile')
            else:
                form.save()
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
