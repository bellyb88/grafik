from .models import *
from django import forms


class PlanForm(forms.ModelForm):
    class Meta:
        model = Dni_swiateczne
        fields = ['data',]


class ProsbaForm(forms.ModelForm):
    class Meta:
        model = Prosba
        fields = ['data', 'dzien', 'noc', 'pracownik']