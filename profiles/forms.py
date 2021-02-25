from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field


class ProfileForm(forms.ModelForm):
    """ Form layout for user profile changes """

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-userform'
        self.helper.form_class = 'form__default'
        self.helper.field_class = 'pb-0 mb-0'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.form_action = '/profile/'
        self.helper.layout = Layout(
            HTML('<p class="small text-muted mb-1">Your Details</p>'),
            Field('first_name', placeholder='First name',
                  css_class="rounded-0"),
            Field('last_name', placeholder='Last name',
                  css_class="rounded-0"),
            Field('email', placeholder='Last name',
                  css_class="rounded-0"),
            HTML('<button id="user-submit" '
                 'class="btn__default mt-2 float-right" title="Update '
                 'profile details"><i class="fas fa-user-alt pr-2" '
                 'aria-hidden="true"></i>Update</button></span>'),
        )

        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
