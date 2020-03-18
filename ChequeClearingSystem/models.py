from django.db import models
from django.contrib.auth.models import User
import datetime
d = datetime.date(1970, 1, 1)


class AccountHolder(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    accountNumber=models.IntegerField(unique=True,default=1000000)
    full_name=models.CharField(max_length=100)
    gender=models.CharField(max_length=1,choices={('M','Male'),('F','Female')})
    fatherName=models.CharField(max_length=100)
    motherName=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    ifsc=models.CharField(max_length=50)
    pan=models.CharField(max_length=10)
    contactNumber=models.IntegerField()
    profilePicture=models.FileField(default='images/male_profile.png')
    dateOfBirth=models.DateField(default=d)


    def __str__(self):
        return self.full_name +'--'+self.pan
