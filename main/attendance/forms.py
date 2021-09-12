from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Employee, EmpLeaveRequests, Notification, Tickets

class TicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = {'content', 'date'}
        widgets = {
            'content': forms.TextInput,
            'date' : forms.SelectDateWidget,
        }

class EmpLeaveAppForm(forms.ModelForm):
    class Meta:
        model = EmpLeaveRequests
        fields = ('content','date_from','date_to')
        
        widgets = {
            'content': forms.TextInput,
            'date_from' : forms.SelectDateWidget,
            'date_to' : forms.SelectDateWidget,
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('content',)
        
        widgets = {
            'content': forms.TextInput,
        }