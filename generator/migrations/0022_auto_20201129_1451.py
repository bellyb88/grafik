# Generated by Django 3.1.3 on 2020-11-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0021_auto_20201126_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grafik',
            name='nazwa',
        ),
        migrations.RemoveField(
            model_name='grafik',
            name='slug',
        ),
        migrations.AlterField(
            model_name='grafik',
            name='data_od',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]
