from django import forms
from django.contrib.auth.models import User

from ChequeClearingSystem.models import AccountHolder


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']


class AccountRegister(forms.ModelForm):
    signature = forms.FileField(widget=forms.FileInput())
    email = forms.EmailField(widget=forms.EmailInput())
    dateOfBirth = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = AccountHolder
        fields = ['accountNumber', 'full_name', 'gender', 'fatherName', 'motherName', 'email', 'ifsc', 'pan',
                  'contactNumber',
                  'profilePicture', 'dateOfBirth', 'signature']
