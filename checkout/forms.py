from django import forms
from .models import Order

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field


class OrderForm(forms.ModelForm):
    """ Form layout for user details at order checkout """

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        placeholder_text = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Post Code',
            'county': 'County, State or Locality',
            'country': 'Country',
            'stripe_pid': 'ref',
        }
        self.helper = FormHelper()
        self.helper.form_id = 'id-orderform'
        self.helper.form_class = 'form__default'
        self.helper.field_class = 'pb-0 mb-0'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = True
        self.helper.form_action = '/checkout/'
        self.helper.layout = Layout(
            HTML('<p class="small text-muted mb-1">Your Details</p>'),
            Field('full_name', css_class="rounded-0"),
            Field('email', css_class="rounded-0"),
            Field('phone_number', css_class="rounded-0"),
            HTML('<p class="small text-muted mt-3 mb-1">Delivery Details</p>'),
            Field('street_address1', css_class="rounded-0"),
            Field('street_address2', css_class="rounded-0"),
            Row(
                Column(Field('town_or_city', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0'),
                Column(Field('county', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0 pl-0-sm'),
                css_class='form-row'),
            Row(
                Column(Field('postcode', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0'),
                Column(Field('country', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0 pl-0-sm'),
                css_class='form-row'
            ),
            Field('stripe_pid', type='hidden'),
            HTML('<p class="small text-muted mt-3 mb-1">Card Details</p>'),
            HTML('<div id="card-element">'
                 '<!--Stripe.js injects the Card Element--></div>'),
            HTML('<p id="card-error" role="alert"></p>'),
            HTML('<p class="result-message hidden">Payment succeeded.</p>'),
            HTML('<button id="order-submit" '
                 'class="btn__default mt-2 float-right">'
                 '<span class="hidden" id="spinner">'
                 '<i class="fas fa-spinner fa-spin pr-2"></i>  '
                 'Processing Payment</span>'
                 '<span id="button-text">'
                 '<i class="far fa-credit-card pr-2" aria-hidden="true"></i>'
                 'Pay Now</span></button>'),
        )

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholder_text[field]} *'
                else:
                    placeholder = placeholder_text[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].label = False

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county', 'stripe_pid',)
