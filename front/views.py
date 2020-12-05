from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.text import slugify
from .forms import *
from .models import Profile
from django.contrib import messages

from generator.models import Plan, Dni_swiateczne
from django.views.generic.edit import CreateView, UpdateView


@login_required
def dashboard(request):
    plany = Plan.objects.all().filter(user=request.user)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', 'plany':plany})


class PlanCreate(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanCreateForm
    template_name = 'front/plan_create.html'

    def get_context_data(self, **kwargs):
        data = super(PlanCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['dni_swiateczne'] = DzienSwiatecznyFormSet(self.request.POST)
        else:
            data['dni_swiateczne'] = DzienSwiatecznyFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        daty = context['dni_swiateczne']
        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.slug = slugify(form.instance.nazwa)
            self.object = form.save()
            if daty.is_valid():
                daty.instance = self.object
                daty.save()
        return super(PlanCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('front:dashboard')


class PlanUpdate(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanCreateForm
    template_name = 'front/plan_update.html'

    def get_context_data(self, **kwargs):
        data = super(PlanUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['dni_swiateczne'] = DzienSwiatecznyFormSet(self.request.POST, instance=self.object)
        else:
            data['dni_swiateczne'] = DzienSwiatecznyFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        daty = context['dni_swiateczne']
        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.slug = slugify(form.instance.nazwa)
            self.object = form.save()
            if daty.is_valid():
                daty.instance = self.object
                daty.save()
        return super(PlanUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('front:plan_update',  kwargs={'pk': self.object.pk})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Uaktualnienie profilu ' \
                                      'zakończyło się sukcesem.')
        else:
            messages.error(request, 'Wystąpił błąd podczas uaktualniania profilu.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika, ale jeszcze nie zapisujemy go w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Zapisanie obiektu User.
            new_user.save()
            # Utworzenie profilu użytkownika.
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
