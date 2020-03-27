from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserForm, LoginForm, AccountRegister, chequeUpload
from .models import bearerBank


class UserFormView(View):
    form_class = UserForm
    template_name = 'ChequeClearingSystem/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("login")
                    return render(request, 'ChequeClearingSystem/details.html', {'form': chequeUpload()})

            return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'ChequeClearingSystem/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("Login")
                    return render(request, 'ChequeClearingSystem/details.html', {'form': chequeUpload()})

        return render(request, 'ChequeClearingSystem/login.html', {'form': form})


@login_required(login_url='/main')
def logout_view(request):
    logout(request)
    print("logout")
    return redirect('ChequeClearingSystem:main')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/main')
def createAccountHolder(request):
    print('c')
    if not request.user.is_authenticated:
        print('a')
        return render(request, 'ChequeClearingSystem/login.html')
    else:
        form = AccountRegister(request.POST or None)
        print('s')
        if form.is_valid():
            print('d')
            # accountHolder = form.save(commit=False)
            accountNumber = form.cleaned_data['accountNumber']
            name = form.cleaned_data['name']
            fatherName = form.cleaned_data['fatherName']
            contactNumber = form.cleaned_data['contactNumber']
            email = form.cleaned_data['email']
            if (bearerBank.objects is None):
                print('None', accountNumber, name)
            print('YEs')
            bankAccount = bearerBank.objects.filter(accountNumber=accountNumber)
            print("Yesssssssssssssss")
            accountOfUser = list()
            for accounts in bankAccount:
                accountOfUser.append((accounts.accountNumber, accounts.full_name, accounts.fatherName,
                                      accounts.contactNumber, accounts.email))
            enteredData = (accountNumber, name, fatherName, contactNumber, email)
            print(enteredData)
            print(accountOfUser)
            print(bankAccount)
            bankAccount = bankAccount.values()
            bankAccount = list(bankAccount)
            bankAccount = bankAccount[0]
            temp = bankAccount
            bankAccount = list()
            for x in temp:
                bankAccount.append(temp[x])

            bankAccount = bearerBank(*bankAccount)
            print(bankAccount)
            if (enteredData == accountOfUser[0] and bankAccount.registered is False):
                print('a')
                bankAccount.registered = True
                print('matched')
                bankAccount.user = request.user
                bankAccount.save(update_fields=['registered', 'user'])
                messages.info(request, 'Your account has been added successfully!')
                return render(request, 'ChequeClearingSystem/details.html', {'form': chequeUpload})
            else:
                messages.info(request, 'Data Not Matched!/Account Exists Already')

        context = {
            "form": AccountRegister(),
        }
        messages.info(request, 'Data Entered is Invalid')
        print('F', form.errors)
        return render(request, 'ChequeClearingSystem/new_account.html', context)

@login_required(login_url='/main')
def details(request):
    if not request.user.is_authenticated:
        return render(request, 'ChequeClearingSystem/login.html')
    elif request.GET == True:
        return render(request, 'ChequeClearingSystem/details.html', {'form': chequeUpload()})

    else:
        form = chequeUpload(request.POST or None, request.FILES or None)
        if form.is_valid():
            chequeDetails = form.save(commit=False)
            chequeDetails.accountNumber = form.cleaned_data['accountNumber']
            chequeDetails.amount = form.cleaned_data['amount']
            chequeDetails.cheque = request.FILES['cheque']
            file_type_sign = chequeDetails.cheque.url.split('.')[-1]
            file_type_sign = file_type_sign.lower()
            accountHolder = bearerBank.objects.filter(user=request.user)
            accountNumberUser = list()
            for accounts in accountHolder:
                accountNumberUser.append(accounts.accountNumber)
            if chequeDetails.accountNumber not in accountNumberUser:
                context = {
                    'chequeDetails': chequeDetails,
                    'form': form,
                    'error_message': 'No account',
                }
                return render(request, 'ChequeClearingSystem/details.html', context)
            accountHolder = bearerBank.objects.filter(accountNumber=chequeDetails.accountNumber)
            accountHolder = accountHolder.values()
            accountHolder = list(accountHolder)
            accountHolder = accountHolder[0]
            temp = accountHolder
            accountHolder = list()
            for x in temp:
                accountHolder.append(temp[x])

            accountHolder = bearerBank(*accountHolder)
            chequeDetails.client = accountHolder
            if file_type_sign not in IMAGE_FILE_TYPES:
                context = {
                    'chequeDetails': chequeDetails,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'ChequeClearingSystem/details.html', context)
            chequeDetails.save()
            return render(request, 'ChequeClearingSystem/details.html',
                          {'chequeDetails': chequeDetails, 'form': chequeUpload()})
        context = {
            "form": form
        }
        return render(request, 'ChequeClearingSystem/details.html', context)
