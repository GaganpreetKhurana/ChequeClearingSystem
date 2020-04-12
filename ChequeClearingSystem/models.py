import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

d = datetime.date(1970, 1, 1)


class AccountHolder(models.Model):
    accountNumber = models.IntegerField(unique=True, default=1000000, verbose_name='Account Number')
    full_name = models.CharField(max_length=100, verbose_name='Name')
    gender = models.CharField(max_length=1, choices={('M', 'Male'), ('F', 'Female')}, verbose_name='Gender')
    fatherName = models.CharField(max_length=100, verbose_name='Father\'s Name')
    motherName = models.CharField(max_length=100, verbose_name='Mother\'s Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    pan = models.CharField(max_length=10, verbose_name='PAN Number')
    contactNumber = models.IntegerField(verbose_name='Contact Number')
    profilePicture = models.FileField(default='images/male_profile.png', verbose_name='Photograph')
    signature = models.FileField(default='images/female.jpg', verbose_name='Signature')
    dateOfBirth = models.DateField(default=d, verbose_name='Date of Birth')
    balance = models.IntegerField(default=10000, verbose_name='Balance')
    lastTransaction = models.DateField(verbose_name='Last Transaction', null=True, blank=True, default=None)

    class Meta:
        abstract = True


class cheque(models.Model):
    cheque = models.FileField(verbose_name='Cheque Image')
    amount = models.IntegerField(verbose_name='Amount')
    accountNumber = models.IntegerField(verbose_name='Account Number')

    class Meta:
        abstract = True


class payeeBank(AccountHolder):

    def __str__(self):
        return self.full_name + '--' + str(self.accountNumber) + '--' + str(self.contactNumber)


class bearerBank(AccountHolder):
    user = models.OneToOneField(User, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    registered = models.BooleanField(default=False, verbose_name='Account Registered')

    def __str__(self):
        return self.full_name + '--' + str(self.accountNumber) + '--' + str(self.contactNumber)


class payeeBankCheque(cheque):
    timeDeposited = models.DateTimeField(default=now, verbose_name='Time Deposited')
    payee = models.ForeignKey(payeeBank, default=1, on_delete=models.DO_NOTHING, verbose_name='Payee')
    bearer = models.ForeignKey(bearerBank, default=1, on_delete=models.DO_NOTHING, verbose_name='Bearer')

    def __str__(self):
        return str(self.accountNumber) + ' ' + str(self.amount) + " " + str(self.timeDeposited)


class bearerBankCheque(cheque):
    timeDeposited = models.DateTimeField(default=now, verbose_name='Time Deposited')
    payee = models.ForeignKey(payeeBank, default=1, on_delete=models.DO_NOTHING, verbose_name='Payee')
    bearer = models.ForeignKey(bearerBank, default=1, on_delete=models.DO_NOTHING, verbose_name='Bearer')

    def __str__(self):
        return str(self.accountNumber) + ' ' + str(self.amount) + ' ' + str(self.timeDeposited)
