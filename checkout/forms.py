from django import forms
from .models import Order

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field


class OrderForm(forms.ModelForm):

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
            HTML('<p class="small text-muted mt-3 mb-1">Delivery Details</p>'),
            Field('street_address1', css_class="rounded-0"),
            Field('street_address2', css_class="rounded-0"),
            Row(
                Column(Field('town_or_city', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0'),
                Column(Field('county', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0 pl-0 pr-1'),
                css_class='form-row'),
            Row(
                Column(Field('postcode', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0'),
                Column(Field('country', css_class="rounded-0"),
                       css_class='form-group col-sm-6 mb-0 pl-0 pr-1'),
                css_class='form-row'
            ),
            HTML('<button type="submit" '
                 'class="btn btn-primary rounded-0 mt-2 float-right">'
                 '<i class="fas fa-lock icon" aria-hidden="true"></i>'
                 'Make Payment</button>'),
        )

        # self.helper.add_input(Submit('submit', 'Make Payment'))

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
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
                  'county',)

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('full_name', 'email', 'phone_number',
#                   'street_address1', 'street_address2',
#                   'town_or_city', 'postcode', 'country',
#                   'county',)

#     def __init__(self, *args, **kwargs):
#         """
#         Use placeholders and remove the default crispy labels
#         """
#         super().__init__(*args, **kwargs)
#         placeholder_text = {
#             'full_name': 'Full Name',
#             'email': 'Email Address',
#             'phone_number': 'Phone Number',
#             'street_address1': 'Street Address 1',
#             'street_address2': 'Street Address 2',
#             'town_or_city': 'Town or City',
#             'postcode': 'Post Code',
#             'county': 'County, State or Locality',
#             'country': 'Country',
#         }

#         self.fields['full_name'].widget.attrs['autofocus'] = True
#         for field in self.fields:
#             if self.fields[field].required:
#                 placeholder = f'{placeholder_text[field]} *'
#             else:
#                 placeholder = placeholder_text[field]
#             self.fields[field].widget.attrs['placeholder'] = placeholder
#             self.fields[field].label = False
