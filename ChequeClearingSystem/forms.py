from django import forms
from django.contrib.auth.models import User

from ChequeClearingSystem.models import bearerBankCheque, bearerBank


class UserForm(forms.ModelForm):
    '''
    User Form for registering new user
    '''
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
    '''
    Login Form
    '''
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    fields = ['username', 'password']


class AccountRegister(forms.Form):
    '''
    Form to register bank account with user
    '''
    name = forms.CharField(widget=forms.TextInput())
    fatherName = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput)
    contactNumber = forms.IntegerField(widget=forms.NumberInput())
    accountNumber = forms.IntegerField(widget=forms.NumberInput())

    class Meta:
        model = bearerBank
        fields = ['accountNumber', 'name', 'fatherName', 'email', 'contactNumber']


class chequeUpload(forms.ModelForm):
    '''
    Form for accepting cheque
    '''
    cheque = forms.FileField(widget=forms.FileInput())
    accountNumber = forms.IntegerField()

    class Meta:
        model = bearerBankCheque
        fields = ['accountNumber', 'amount', 'cheque']
