from .models import *
from django import forms


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'priority', 'last_state')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)