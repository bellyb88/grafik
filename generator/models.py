from django.db import models
from django.contrib.auth.models import User


# Create your models here.
DZIEN_CHOICES = (('None','None'), ('0','Poniedzialek'), ('1','Wtorek'), ('2','Sroda'), ('3','Czwartek'), ('4','Piatek'), ('5','Sobota'), ('6','Niedziela'),('14','Pon-Pt'),('15','Pon-Sb'), ('56','Weekend'), ('Wszystkie','Wszystkie'),  )


class Plan(models.Model):
    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = "Plany"

    nazwa = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Dni_swiateczne(models.Model):
    class Meta:
        verbose_name = 'Dzień świąteczny'
        verbose_name_plural = "Dni świąteczne"

    data = models.DateField(blank=True, null=True)
    dni_swiateczne = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='dni_swiateczne')


class Regula(models.Model):
    class Meta:
        verbose_name = 'Reguła'
        verbose_name_plural = "Reguły"

    nazwa = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    ilosc_pracownikow_dzien = models.SmallIntegerField(default=3)
    ilosc_pracownikow_noc = models.SmallIntegerField(default=2)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    dzien = models.CharField(max_length=19, choices=DZIEN_CHOICES)
    data_od = models.DateField(blank=True, null=True)
    data_do = models.DateField(blank=True, null=True)




class Pracownik(models.Model):
    class Meta:
        verbose_name = 'Pracownik'
        verbose_name_plural = "Pracownicy"

    numer = models.SmallIntegerField(db_index=True)
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    email = models.EmailField(blank = True)
    adres = models.TextField(max_length=500, blank = True)
    ilosc_godzin = models.SmallIntegerField(default=160)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numer)

class Prosba(models.Model):
    class Meta:
        verbose_name = 'Prośba'
        verbose_name_plural = 'Prośby'

    dzien = models.BooleanField()
    noc = models.BooleanField()
    data =  models.DateField(blank=True, null=True)
    pracownik = models.ForeignKey(Pracownik, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pracownik.nazwisko)+ ' '+str(self.data)


class Grafik(models.Model):
    class Meta:
        verbose_name = 'Grafik'
        verbose_name_plural = "Grafiki"

    data_od = models.DateField(blank=True, null=True, db_index=True)
    data_do = models.DateField(blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data_od)+ ' - '+str(self.data_do)

class Doba(models.Model):
    class Meta:
        verbose_name ='Doba'
        verbose_name_plural = "Doby"

    data = models.DateField(db_index=True)
    pracownicy_dzien = models.ManyToManyField(Pracownik, related_name='pracownicy_dzien')
    pracownicy_noc = models.ManyToManyField(Pracownik, related_name='pracownicy_noc')
    min_pracownicy_dzien = models.SmallIntegerField(null=True, blank=True)
    min_pracownicy_noc = models.SmallIntegerField(null=True, blank=True)
    swieto = models.BooleanField(default=False)
    grafik = models.ForeignKey(Grafik, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.data) + str(self.pracownicy_dzien.all())