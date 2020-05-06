from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from ChequeClearingSystemProject.settings import BASE_DIR
from confirmationMessages import sendMessage
from processing import processing
from .forms import UserForm, LoginForm, AccountRegister, chequeUpload
from .models import bearerBank, payeeBank, payeeBankCheque


class UserFormView(View):
    '''
    form view to registering new user
    '''
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
    '''
    form view for Login
    '''
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
    '''
    logout view
    :param request: request object
    :return: redirects to login
    '''
    logout(request)
    print("logout")
    return redirect('ChequeClearingSystem:main')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/main')
def createAccountHolder(request):
    '''
    To register account with user
    :param request: request object
    :return: redirects to login page ,details page,register account page
    '''
    if not request.user.is_authenticated:  # unauthenticated user
        return render(request, 'ChequeClearingSystem/login.html')
    else:
        form = AccountRegister(request.POST or None)
        if form.is_valid():  # check if form is valid
            # extract detais
            accountNumber = form.cleaned_data['accountNumber']
            name = form.cleaned_data['name']
            fatherName = form.cleaned_data['fatherName']
            contactNumber = form.cleaned_data['contactNumber']
            email = form.cleaned_data['email']

            # get details from bearerBank database and check if account exists
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

            # registers account
            if (enteredData == accountOfUser[0] and bankAccount.registered is False):
                bankAccount.registered = True
                bankAccount.user = request.user
                bankAccount.save(update_fields=['registered', 'user'])
                return redirect('ChequeClearingSystem:profile')

        # for unregistered account
        context = {
            "form": AccountRegister(),
        }
        messages = 'Data Entered is Invalid'
        context['msg'] = messages
        return render(request, 'ChequeClearingSystem/new_account.html', context)


@login_required(login_url='/main')
def details(request):
    '''
    to display user details and accept the cheque
    :param request:
    :return: redirects to appropriate page
    '''
    # get user account details from database
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

    if not request.user.is_authenticated:  # unauthenticated user
        return redirect('ChequeClearingSystem:main')
    elif request.POST:  # post request
        form = chequeUpload(request.POST or None, request.FILES or None)
        if form.is_valid():
            # extract details and files from form
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

            # cheque if account exists in database and user is registered with that account
            if chequeDetails.accountNumber not in accountNumberUser:
                context = {
                    'chequeDetails': chequeDetails,
                    'form': chequeUpload(),
                    'msg': 'No account',
                    'details': details
                }
                return render(request, 'ChequeClearingSystem/details.html', context)

            # Create entry in bearer bank database
            accountHolder = bearerBank.objects.filter(accountNumber=chequeDetails.accountNumber)
            accountHolder = accountHolder.values()
            accountHolder = list(accountHolder)
            accountHolder = accountHolder[0]
            temp = accountHolder
            accountHolder = list()

            for x in temp:
                accountHolder.append(temp[x])

            accountHolder = bearerBank(*accountHolder)
            chequeDetails.bearer = accountHolder

            # check file type
            if file_type_sign not in IMAGE_FILE_TYPES:
                context = {
                    'chequeDetails': chequeDetails,
                    'form': form,
                    'msg': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'ChequeClearingSystem/details.html', context)
            chequeDetails.chequeNumber = -1

            # extract details and match them with the database
            try:
                chequeDetails.save()

                acknowledgement = processing(chequeDetails.amount,
                                             BASE_DIR + '/ChequeClearingSystem/files/' + str(chequeDetails.cheque),
                                             accountHolder.full_name)
            except:
                acknowledgement = 'NAK'

            if acknowledgement == 'NAK':  # invalid Format
                message = 'Transaction Failed'
                return render(request, 'ChequeClearingSystem/details.html',
                              {'chequeDetails': chequeDetails, 'form': chequeUpload(), 'details': details,
                               'msg': message})
            elif acknowledgement[0] == 'NAK':  # Details verification failed
                try:
                    message = 'Transaction Failed. Balance in A/C ' + str(acknowledgement[3]) + ": " + str(
                        acknowledgement[2])
                    sendMessage(contactNumber=acknowledgement[1], msg=message)  # send the message to payee
                    message = 'Transaction Failed. Balance in A/C ' + str(accountHolder.accountNumber) + ": " + str(
                        accountHolder.balance)

                    sendMessage(contactNumber=accountHolder.contactNumber, msg=message)  # send the message to bearer
                except:
                    message = "Transaction Failed"

                return render(request, 'ChequeClearingSystem/details.html',
                              {'chequeDetails': chequeDetails, 'form': chequeUpload(), 'details': details,
                               'msg': message})
            else:
                try:
                    # payeeBank object for entry in payee Bank Database
                    payee = payeeBank.objects.filter(accountNumber=acknowledgement[1])
                    payee = payee.values()
                    payee = list(payee)
                    payee = payee[0]
                    temp = payee
                    payee = list()
                    for x in temp:
                        payee.append(temp[x])

                    payee = payeeBank(*payee)
                    chequeDetails.payee = payee
                    chequeDetails.chequeNumber = acknowledgement[3]

                    timeNow = datetime.now()
                    accountHolder.lastTransaction = timeNow
                    payee.lastTransaction = timeNow
                    accountHolder.balance += acknowledgement[2]
                    payee.balance -= acknowledgement[2]

                    # payeeBankCheque object for entry in payeeBank cheque database
                    payeeCheque = payeeBankCheque()
                    payeeCheque.payee = payee
                    payeeCheque.bearer = accountHolder
                    payeeCheque.cheque = chequeDetails.cheque
                    payeeCheque.chequeNumber = acknowledgement[3]
                    payeeCheque.timeDeposited = timeNow
                    payeeCheque.amount = chequeDetails.amount

                    # save
                    chequeDetails.save()
                    accountHolder.save()
                    payee.save()
                    payeeCheque.save()

                    # send message to bearer and payee
                    sendMessage(acknowledgement[2], accountHolder.balance, accountHolder.contactNumber,
                                accountHolder.accountNumber)
                    sendMessage(-acknowledgement[2], payee.balance, payee.contactNumber, payee.accountNumber)
                    message = 'Transaction Successful'
                except:
                    message = "Transaction Failed"
                return render(request, 'ChequeClearingSystem/details.html',
                              {'chequeDetails': chequeDetails, 'form': chequeUpload(), 'details': details,
                               'msg': message})

        return redirect('ChequeClearingSystem:profile')
    else:  # for get request
        if details is not None:  # user has account registered
            message = "WELCOME " + details['name']
        else:
            message = "WELCOME"
        return render(request, 'ChequeClearingSystem/details.html',
                      {'form': chequeUpload(), 'details': details, 'msg': message})
