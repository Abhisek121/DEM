from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    @property
    def is_employee(self):
        if hasattr(self, 'employee'):
            return True
        return False

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_id=models.BigIntegerField()
    name=models.CharField(max_length=60, blank=True, null=True)
    phone=models.BigIntegerField(blank=True, null=True)
    department=models.CharField(max_length=60, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    address=models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        '''if self.name==None:
            return str(self.card_id)
        else:
            return str(self.name) + ' : ' + str(self.card_id)'''
        return str(self.name)

class Record(models.Model):
    emp = models.ManyToManyField(Employee)
    ids=models.IntegerField(default=0)
    card_id=models.BigIntegerField()
    name=models.CharField(max_length=60, blank=True, null=True)
    department=models.CharField(max_length=60, blank=True, null=True)
    date=models.DateField(default=datetime.date.today)
    time_in=models.TimeField(default=datetime.datetime.now())
    time_out=models.TimeField(blank=True, null=True)
    status=models.TextField(max_length=100)

    def __str__(self):
        return str(self.name) + ' : ' + str(self.date)

class EmpLeaveRequests(models.Model):
    remp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date_from = models.DateField(max_length= 100, default=None)
    date_to = models.DateField(max_length=100, default=None)
    status = models.CharField(max_length=100, null=True)

class AppStatus(models.Model):
    leaveApp = models.ForeignKey(EmpLeaveRequests, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True)

class Notification(models.Model):
    content = models.CharField(max_length=1000, null=True)
    date=models.DateField(default=datetime.date.today)

class Tickets(models.Model):
    temp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date = models.DateField(max_length= 100, default=None)
    status = models.CharField(max_length=100, null=True)