from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from avatar.models import Avatar

class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user



class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_class = 'form-control'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name')

class AvatarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_class = 'form-control'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Avatar
        fields = ('avatar', 'primary')