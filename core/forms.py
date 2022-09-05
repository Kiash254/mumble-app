from django.forms import ModelForm
from .models import *


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants', 'host']


class Userform(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']