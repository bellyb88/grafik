# Generated by Django 3.1.3 on 2020-11-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0010_auto_20201125_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dniowka',
            name='min_pracownicy',
        ),
        migrations.AddField(
            model_name='dniowka',
            name='min_pracownicy_dzien',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dniowka',
            name='min_pracownicy_noc',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
