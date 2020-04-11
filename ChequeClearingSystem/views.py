from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserForm, LoginForm, AccountRegister, chequeUpload
from .models import bearerBank
from .static.processing import extractDetails


class UserFormView(View):
    form_class = UserForm
    template_name = 'ChequeClearingSystem/registration_form.html'

    def get(self, request):
        logout(request)
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
                    return redirect('ChequeClearingSystem:profile')

            return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'ChequeClearingSystem/login.html'

    def get(self, request):
        logout(request)
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
                    return redirect('ChequeClearingSystem:profile')
        return redirect('ChequeClearingSystem:main')


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
        return render(request, 'ChequeClearingSystem/login.html')
    else:
        form = AccountRegister(request.POST or None)
        if form.is_valid():
            accountNumber = form.cleaned_data['accountNumber']
            name = form.cleaned_data['name']
            fatherName = form.cleaned_data['fatherName']
            contactNumber = form.cleaned_data['contactNumber']
            email = form.cleaned_data['email']
            if (bearerBank.objects is None):
                print('None', accountNumber, name)
            bankAccount = bearerBank.objects.filter(accountNumber=accountNumber)
            accountOfUser = list()
            for accounts in bankAccount:
                accountOfUser.append((accounts.accountNumber, accounts.full_name, accounts.fatherName,
                                      accounts.contactNumber, accounts.email))
            enteredData = (accountNumber, name, fatherName, contactNumber, email)
            bankAccount = bankAccount.values()
            bankAccount = list(bankAccount)
            bankAccount = bankAccount[0]
            temp = bankAccount
            bankAccount = list()
            for x in temp:
                bankAccount.append(temp[x])

            bankAccount = bearerBank(*bankAccount)
            if (enteredData == accountOfUser[0] and bankAccount.registered is False):
                bankAccount.registered = True
                bankAccount.user = request.user
                bankAccount.save(update_fields=['registered', 'user'])
                messages.info(request, 'Your account has been added successfully!')
                return redirect('ChequeClearingSystem:profile')
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
    # get user acccount details from database
    print("YYYYYYYYY")
    profile = bearerBank.objects.filter(user=request.user, registered=True)
    details = None
    if profile:
        details = dict()
        profile = profile[0]
        details['accountNumber'] = profile.accountNumber
        details['name'] = profile.full_name
        details['fatherName'] = profile.fatherName
        details['balance'] = profile.balance
        details['profilePicture'] = profile.profilePicture.url
        details['dateOfBirth'] = profile.dateOfBirth
        details['pan'] = profile.pan

    print(request.user)
    print(details)
    if not request.user.is_authenticated:
        print('No')
        return redirect('ChequeClearingSystem:main')
    elif request.POST:
        print("X")
        form = chequeUpload(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("XX")
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
                    'form': chequeUpload(),
                    'error_message': 'No account',
                    'details': details
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
            detailsFromCheque = extractDetails.extractDetailsFromCheque(
                './static/processing/cheque.png')  # chequeDetails.cheque)
            print(detailsFromCheque)

            return render(request, 'ChequeClearingSystem/details.html',
                          {'chequeDetails': chequeDetails, 'form': chequeUpload(), 'details': details})

        return redirect('ChequeClearingSystem:profile')
    else:
        print("yes")
        return render(request, 'ChequeClearingSystem/details.html', {'form': chequeUpload(), 'details': details})
