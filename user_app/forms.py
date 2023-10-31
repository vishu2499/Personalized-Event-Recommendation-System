from django import forms
from user_app.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.Form):

    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=12,required=False)
    # age = forms.IntegerField(min_value=1,max_value=130)
    # birth_date = forms.DateField()
