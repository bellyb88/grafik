from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, ModelChoiceField, SelectDateWidget, DateInput


from .models import Profile
from generator.models import Plan, Dni_swiateczne, Regula, Urlop, Pracownik, Prosba
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


class UrlopForm(forms.ModelForm):
    class Meta:
        model = Urlop
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UrlopForm, self).__init__(*args, **kwargs)
        self.fields['data_od'] = forms.DateField(widget = SelectDateWidget())
        self.fields['data_do'] = forms.DateField(widget = SelectDateWidget())



UrlopFormSet = inlineformset_factory(
    parent_model=Pracownik, model=Urlop, form=UrlopForm,
    fields=['data_od', 'data_do' ], extra=1, can_delete=True)


class PracownikUrlopForm(forms.ModelForm):

    class Meta:
        model = Pracownik
        fields = []

    def __init__(self, *args, **kwargs):
        super(PracownikUrlopForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(

                Fieldset('Dodaj daty urlopu',
                    Formset('urlopy')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Zapisz')),
                )
            )







class ProsbaForm(forms.ModelForm):
    class Meta:
        model = Prosba
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProsbaForm, self).__init__(*args, **kwargs)
        self.fields['data'] = forms.DateField(widget = SelectDateWidget())




ProsbaFormSet = inlineformset_factory(
    parent_model=Pracownik, model=Prosba, form=ProsbaForm,
    fields=['data', 'dzien', 'noc' ], extra=1, can_delete=True)


class PracownikProsbaForm(forms.ModelForm):

    class Meta:
        model = Pracownik
        fields = []

    def __init__(self, *args, **kwargs):
        super(PracownikProsbaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(

                Fieldset('Dodaj daty próśb',
                    Formset('prosby')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Zapisz')),
                )
            )










class DniSwiateczneForm(forms.ModelForm):

    class Meta:
        model = Dni_swiateczne
        fields = ['data',]

    def __init__(self, *args, **kwargs):
        super(DniSwiateczneForm, self).__init__(*args, **kwargs)
        self.fields['data'] = forms.DateField(widget = DateInput(format=('%d-%m-%Y')))


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


class RegulaForm(forms.ModelForm):
    class Meta:
        model = Regula
        fields = ['nazwa', 'plan', 'ilosc_pracownikow_dzien', 'ilosc_pracownikow_noc', 'dzien', 'data_od', 'data_do']

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop("user")
        super(RegulaForm, self).__init__(*args, **kwargs)
        self.fields['plan'] =  ModelChoiceField(queryset=Plan.objects.all().filter(user = user))

