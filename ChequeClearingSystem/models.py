import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

d = datetime.date(1970, 1, 1)


class AccountHolder(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    accountNumber = models.IntegerField(unique=True, default=1000000)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices={('M', 'Male'), ('F', 'Female')})
    fatherName = models.CharField(max_length=100)
    motherName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ifsc = models.CharField(max_length=50)
    pan = models.CharField(max_length=10)
    contactNumber = models.IntegerField()
    profilePicture = models.FileField(default='images/male_profile.png')
    signature = models.FileField(default='images/female.jpg')
    dateOfBirth = models.DateField(default=d)
    balance = models.IntegerField(default=10000)
    registered = models.BooleanField(default=False)
    class Meta:
        abstract = True


class cheque(models.Model):
    cheque = models.FileField()
    amount = models.IntegerField()
    accountNumber = models.IntegerField()

    class Meta:
        abstract = True


class payeeBank(AccountHolder):

    def __str__(self):
        return self.full_name + '--' + self.pan


class bearerBank(AccountHolder):
    def __str__(self):
        return self.full_name + '--' + self.pan


class payeeBankCheque(cheque):
    timeDeposited = models.DateTimeField(default=now)
    client = models.ForeignKey(payeeBank, default=1, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.accountNumber) + str(self.amount) + str(self.timeDeposited)


class bearerBankCheque(cheque):
    timeDeposited = models.DateTimeField(default=now)
    client = models.ForeignKey(bearerBank, default=1, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.accountNumber) + str(self.amount) + str(self.timeDeposited)
