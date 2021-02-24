from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field

from products.models import ProductReviews


class ReviewForm(forms.ModelForm):
    """ Crispy form for Product reviews """

    def __init__(self, *args, **kwargs):
        self.is_add = kwargs.pop("is_add", False)
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-reviewform'
        self.helper.form_class = 'form__default'
        self.helper.field_class = 'pb-0 mb-0'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.form_action = '/reviews/'
        self.helper.layout = Layout(
            Field('comment', placeholder='Review comment',
                  rows='4', css_class="rounded-0"),
            Row(
                Column(HTML(' ' if self.is_add else '<div class="'
                            'custom-control custom-checkbox float-right">'
                            '<input type="checkbox" id="delete-review" class'
                            '="review__checkbox custom-control-input" name="'
                            'delete-review" value="1"><label class="'
                            'review__checkbox custom-control-label" for="'
                            'delete-review">Delete review</label></div>'),
                       css_class='form-group col-12 mb-0'),
                css_class='form-row mt-2'),
            Row(
                Column(HTML('<p class="mb-0">Review rating</p>'),
                       css_class='form-group col-12 mb-0'),
                css_class='form-row'),
            Row(
                Column(Field('rating', placeholder='Set rating',
                             css_class="rounded-0"),
                       css_class='form-group col-5 mb-0'),
                Column(HTML('<button id="user-submit" '
                            'class="btn__default mt-0 float-right">'
                            '<i class="far fa-file-alt d-none d-sm-inline" '
                            'aria-hidden="true">'
                            '</i><span class="pl-1">'),
                       HTML('Add Review' if self.is_add else
                            'Update Review</button></span>'),
                       css_class='form-group col-7 mb-0'),
                css_class='form-row'),
        )

        self.fields['comment'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductReviews
        fields = ('comment', 'rating', 'product', 'user')
