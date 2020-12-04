from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import calendar
import datetime
import random
from .models import *



# Create your views here.



def oblicz_kalendarz(plan, data):
    kalendarz = calendar.Calendar()
    dni_swiateczne = [x.data for x in plan.dni_swiateczne.all()]
    kalend = []

    for i in range(3):
        kalend_bez_dat =kalendarz.itermonthdays2(year=data.year, month=data.month)

        for x in [tuple(reversed(x)) + (data.month, data.year) for x in kalend_bez_dat if x[0] != 0]:
            b = datetime.date(year=x[-1], month=x[-2], day=x[-3])
            if b in dni_swiateczne:
                a = 6
            else:
                a = x[0]
            c = [a, b]
            kalend.append(c)
        data = data + datetime.timedelta(days=31)


    wartosci_dni = {}
    for regula in plan.regula_set.filter(dzien = 'Wszystkie'):
        for x in range(7):
            wartosci_dni[x] = [regula.ilosc_pracownikow_dzien, regula.ilosc_pracownikow_noc]
    for regula in plan.regula_set.filter(dzien = '15'):
        for x in range(6):
            wartosci_dni[x] = [regula.ilosc_pracownikow_dzien, regula.ilosc_pracownikow_noc]

    for regula in plan.regula_set.filter(dzien= '14'):
        for x in range(5):
            wartosci_dni[x] = [regula.ilosc_pracownikow_dzien, regula.ilosc_pracownikow_noc]

    for regula in plan.regula_set.filter(dzien= '56'):
        val = [regula.ilosc_pracownikow_dzien, regula.ilosc_pracownikow_noc]
        wartosci_dni[5] = val
        wartosci_dni[6] = val

    for regula in plan.regula_set.filter(dzien__in = range(7)):
        val= [regula.ilosc_pracownikow_dzien, regula.ilosc_pracownikow_noc]
        for x in range(7):
            if int(regula.dzien) == x:
                wartosci_dni[x] = val


    pn_pt = [x for x in kalend if x[0] in [0,1,2,3,4]]
    pn_sb = [x for x in kalend if x[0] in [0, 1, 2, 3, 4, 5]]
    nd = [x for x in kalend if x[0] == 6]
    ilosc_zmian_pn_sb_dzien = [ wartosci_dni[x[0]][0] for x in pn_sb]
    ilosc_zmian_pn_sb_noc = [ wartosci_dni[x[0]][1] for x in pn_sb]
    [x.append(wartosci_dni.get(x[0])) for x in kalend]

    grafik = Grafik.objects.create(data_od=kalend[0][1], data_do=kalend[-1][1],
                                   plan=plan)

    for doba in kalend:
        if doba[0] == 6:
            x=True
        else:
            x=False
        Doba.objects.create(data = doba[1], grafik=grafik, swieto=x,
                            min_pracownicy_dzien = doba[2][0], min_pracownicy_noc = doba[2][1])


    for regula in plan.regula_set.filter(dzien='None'):
        for doba in Doba.objects.all().filter(data__range=[regula.data_od, regula.data_do]):
            doba.min_pracownicy_dzien=  regula.ilosc_pracownikow_dzien
            doba.min_pracownicy_noc = regula.ilosc_pracownikow_noc
            doba.save()

    slownik={}
    slownik['dni_pn_pt'] = len(pn_pt)
    slownik['dni_pn_sb'] = len(pn_sb)
    slownik['dni_nd'] = len(nd)
    slownik['ilosc_godzin'] = len(pn_pt)*(7.5833)
    slownik['ilosc_dyzurow'] = (len(pn_pt)*(7+35/60))/12
    slownik['ilosc_zmian_nd_dzien'] = len(nd) * wartosci_dni[6][0]
    slownik['ilosc_zmian_nd_noc'] = len(nd) * wartosci_dni[6][1]
    slownik['ilosc_zmian_pn_sb_dzien'] = sum(ilosc_zmian_pn_sb_dzien)
    slownik['ilosc_zmian_pn_sb_noc'] = sum(ilosc_zmian_pn_sb_noc)
    slownik['ilosc_zmian'] = slownik['ilosc_zmian_nd_dzien'] + slownik['ilosc_zmian_nd_noc'] +slownik['ilosc_zmian_pn_sb_noc'] + slownik['ilosc_zmian_pn_sb_dzien']
    return kalend, slownik, grafik








def strona_glowna(request, month, year):
    plan = get_object_or_404(Plan, id=1)
    data = datetime.date(day=1,month=month, year=year)
    kalend, slownik, grafik = oblicz_kalendarz(plan, data)

    wszyscy_pracownicy = plan.pracownik_set.all()
    numery_wszystkich_pracownikow = [x.numer for x in wszyscy_pracownicy]
    pula_godzin = slownik.get('ilosc_zmian')*12



    def losuj_dzien(grafik, pracownik, dni):
        doby_wykluczajace = [doba.data for doba in Doba.objects.all().filter(grafik=grafik).filter(
            Q(pracownicy_dzien=pracownik) | Q(pracownicy_noc=pracownik))]
        dni_wykluczajace = [doba.data + datetime.timedelta(days=1) for doba in
                            Doba.objects.all().filter(grafik=grafik).filter(pracownicy_noc=pracownik)]

        dni_zero_miejsc = [doba.data for doba in
                            Doba.objects.all().filter(grafik=grafik).filter(min_pracownicy_dzien=0)]
        prosby = [x.data for x in Prosba.objects.all().filter(pracownik=pracownik).filter(dzien=True)]
        wyklucz = list(doby_wykluczajace + dni_wykluczajace +dni_zero_miejsc +prosby)

        dni_losowe = list(set(dni) - set(wyklucz))
        if dni_losowe == []:
            return None
        data_wylosowana = random.choice(dni_losowe)
        d = get_object_or_404(Doba, grafik=grafik, data=data_wylosowana)
        d.pracownicy_dzien.add(pracownik)
        d.min_pracownicy_dzien = d.min_pracownicy_dzien -1
        d.save()
        return True



    def losuj_noc(grafik, pracownik, dni):
        noce_wykluczajace = [doba.data - datetime.timedelta(days=1) for doba in
                             Doba.objects.all().filter(grafik=grafik).filter(pracownicy_dzien=pracownik)]
        doby_wykluczajace = [doba.data for doba in Doba.objects.all().filter(grafik=grafik).filter(
            Q(pracownicy_dzien=pracownik) | Q(pracownicy_noc=pracownik))]

        dni_zero_miejsc = [doba.data for doba in
                            Doba.objects.all().filter(grafik=grafik).filter(min_pracownicy_noc=0)]
        prosby = [x.data for x in
                  Prosba.objects.all().filter(pracownik=pracownik).filter(noc=True)]
        wyklucz = list(doby_wykluczajace + noce_wykluczajace +dni_zero_miejsc+prosby)
        noce_losowe = list(set(dni) - set(wyklucz))
        if noce_losowe == []:
            return None
        data_wylosowana = random.choice(noce_losowe)

        d = get_object_or_404(Doba, grafik=grafik, data=data_wylosowana)
        d.pracownicy_noc.add(pracownik)
        d.min_pracownicy_noc = d.min_pracownicy_noc -1
        d.save()
        return True


    for pracownik in wszyscy_pracownicy:
        pracownik.ilosc_godzin = slownik.get('ilosc_godzin')
        pracownik.save()




    while True:
        if pula_godzin > 0:
            if len(numery_wszystkich_pracownikow)>0:
                numer = random.choice(numery_wszystkich_pracownikow)
                numery_wszystkich_pracownikow.remove(numer)
            else:
                numery_wszystkich_pracownikow = [x.numer for x in wszyscy_pracownicy]
                numer = random.choice(numery_wszystkich_pracownikow)
                numery_wszystkich_pracownikow.remove(numer)

            pracownik = get_object_or_404(Pracownik, numer=numer)



            reguly = grafik.plan.regula_set.all()

            for regula in reguly:
                if len(regula.dzien) == 1:
                    dni = [x[1] for x in kalend if x[0] == int(regula.dzien)]
                    if losuj_dzien(grafik, pracownik, dni) == True:
                        pula_godzin = pula_godzin - 12
                    if losuj_noc(grafik, pracownik, dni) == True:
                        pula_godzin = pula_godzin - 12


                elif len(regula.dzien) == 2:
                    dni = [x[1] for x in kalend if x[0] in range(int(regula.dzien[0])-1,int(regula.dzien[1])+1)]
                    if losuj_dzien(grafik, pracownik, dni) == True:
                        pula_godzin = pula_godzin - 12
                    if losuj_noc(grafik, pracownik, dni) == True:
                        pula_godzin = pula_godzin - 12
                else:
                    pass

        else:
            return render(request, 'main.html', {'kalend': kalend, })



