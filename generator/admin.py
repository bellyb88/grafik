from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
class ProsbaInline(admin.TabularInline):
    model = Prosba
    form = ProsbaForm

@admin.register(Pracownik)
class PracownikAdmin(admin.ModelAdmin):
    list_display = ['numer','nazwisko','imie','get_dyzury' , 'email','adres']
    prepopulated_fields = {'slug':('nazwisko','imie')}
    inlines = [ProsbaInline,]
  #  list_editable = ['nazwisko', 'imie',  'email', 'adres']
    def get_dyzury(self,obj):
        dzien = len([x for x in obj.pracownicy_dzien.all()])
        noc = len([x for x in obj.pracownicy_noc.all()])
        return dzien, noc, dzien+noc

@admin.register(Regula)
class RegulaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'slug', 'ilosc_pracownikow_dzien','ilosc_pracownikow_noc',  'dzien']
    prepopulated_fields = {'slug': ('nazwa',)}
    list_filter = [ 'dzien']


class PlanInline(admin.TabularInline):
    model = Dni_swiateczne
    form = PlanForm


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nazwa','dni_swiateczne']
    prepopulated_fields = {'slug': ('nazwa',)}
    inlines = [PlanInline,]


@admin.register(Grafik)
class GrafikAdmin(admin.ModelAdmin):
    list_display = ['data_od', 'data_do']

@admin.register(Doba)
class DobaAdmin(admin.ModelAdmin):
    list_display = ['data', 'get_pracownicy_dzien','min_pracownicy_dzien',
                    'get_pracownicy_noc', 'min_pracownicy_noc']

    def get_pracownicy_dzien(self,obj):
        a= [x for x in obj.pracownicy_dzien.all()]
        return a
    def get_pracownicy_noc(self,obj):
        a = [x for x in obj.pracownicy_noc.all()]
        return a

    list_filter = ['grafik']