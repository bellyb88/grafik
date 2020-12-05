from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Profile
from generator.models import Plan, Dni_swiateczne
from .formset import *

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', 
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('PWZ',)





class DniSwiateczneForm(forms.ModelForm):

    class Meta:
        model = Dni_swiateczne
        fields = '__all__'

DzienSwiatecznyFormSet = inlineformset_factory(
    parent_model=Plan, model=Dni_swiateczne, form=DniSwiateczneForm,
    fields='__all__', extra=1, can_delete=True
    )


class PlanCreateForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ['nazwa',]

    def __init__(self, *args, **kwargs):
        super(PlanCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('nazwa'),
                Fieldset('Dodaj daty dni świątecznych',
                    Formset('dni_swiateczne')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Zapisz')),
                )
            )
