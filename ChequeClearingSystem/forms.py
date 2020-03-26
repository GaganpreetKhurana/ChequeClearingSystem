from django import forms
from django.contrib.auth.models import User

from ChequeClearingSystem.models import AccountHolder, bearerBankCheque


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        required = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
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


class chequeUpload(forms.ModelForm):
    cheque = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = bearerBankCheque
        fields = ['accountNumber', 'amount', 'cheque']
