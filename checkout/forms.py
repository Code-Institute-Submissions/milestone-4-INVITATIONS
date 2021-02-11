from django import forms
from .models import Order

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML


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
        self.helper.form_action = 'submit_survey'
        self.helper.layout = Layout('full_name',
                                    'email',
                                    HTML('<p class="mt-3 mb-1">Delivery Details:</p>'),
                                    'street_address1',
                                    'street_address2',
                                    Row(
                                        Column('town_or_city', css_class='form-group col-sm-6 mb-0'),
                                        Column('county', css_class='form-group col-sm-6 mb-0 pl-0 pr-1'),
                                        css_class='form-row'
                                    ),
                                    Row(
                                        Column('postcode', css_class='form-group col-sm-6 mb-0'),
                                        Column('country', css_class='form-group col-sm-6 mb-0 pl-0 pr-1'),
                                        css_class='form-row'
                                    ),)

        self.helper.add_input(Submit('submit', 'Submit'))

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
