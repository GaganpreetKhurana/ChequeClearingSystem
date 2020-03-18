from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserForm, LoginForm, AccountRegister


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
                    return render(request, 'ChequeClearingSystem/logout.html', {'form': form})

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
                    return render(request, 'ChequeClearingSystem/logout.html', {'form': form})
        return render(request, 'ChequeClearingSystem/login.html', {'form': form})


def logout_view(request):
    logout(request)
    print("logout")
    return redirect('ChequeClearingSystem:main')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def createAccountHolder(request):
    print("ajnakn")
    if not request.user.is_authenticated:
        return render(request, 'ChequeClearingSystem/login.html')
    else:
        form = AccountRegister(request.POST or None, request.FILES or None)
        if form.is_valid():
            accountHolder = form.save(commit=False)
            accountHolder.user = request.user
            accountHolder.accountNumber = form.cleaned_data['accountNumber']
            accountHolder.full_name = form.cleaned_data['full_name']
            accountHolder.gender = form.cleaned_data['gender']
            accountHolder.fatherName = form.cleaned_data['fatherName']
            accountHolder.motherName = form.cleaned_data['motherName']
            accountHolder.ifsc = form.cleaned_data['ifsc']
            accountHolder.pan = form.cleaned_data['pan']
            accountHolder.contactNumber = form.cleaned_data['contactNumber']
            accountHolder.email = form.cleaned_data['email']
            accountHolder.dateOfBirth = form.cleaned_data['dateOfBirth']
            accountHolder.profilePicture = request.FILES['profilePicture']
            file_type = accountHolder.profilePicture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'accountHolder': accountHolder,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'ChequeClearingSystem/new_account.html', context)
            accountHolder.save()
            return render(request, 'ChequeClearingSystem/details.html', {'accountHolder': accountHolder})
        context = {
            "form": form,
        }
        return render(request, 'ChequeClearingSystem/new_account.html', context)
