from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field, Submit

from products.models import ProductReviews


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.is_add = kwargs.pop("is_add", False)
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-userform'
        self.helper.form_class = 'form__default'
        self.helper.field_class = 'pb-0 mb-0'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.form_action = '/reviews/'
        self.helper.layout = Layout(
            Field('comment', placeholder='Review comment',
                  rows='4', css_class="rounded-0"),
            HTML('<p class="mt-2 mb-0">Product/Service rating</p>'),
            Field('rating', placeholder='Set rating',
                  css_class="rounded-0"),
            HTML('<button id="user-submit" '
                 'class="btn__default mt-4 float-right">'
                 '<i class="far fa-file-alt" aria-hidden="true"></i>'
                 '<span class="pl-1">'),
            HTML('Add Review' if self.is_add else
                 'Update Review</button></span>'),
        )

        self.fields['comment'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductReviews
        fields = ('comment', 'rating', 'product', 'user')
