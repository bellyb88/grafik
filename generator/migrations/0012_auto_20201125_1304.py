# Generated by Django 3.1.3 on 2020-11-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0011_auto_20201125_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regula',
            name='ilosc_pracownikow',
        ),
        migrations.RemoveField(
            model_name='regula',
            name='pora',
        ),
        migrations.AddField(
            model_name='regula',
            name='ilosc_pracownikow_dzien',
            field=models.SmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='regula',
            name='ilosc_pracownikow_noc',
            field=models.SmallIntegerField(default=2),
        ),
    ]
