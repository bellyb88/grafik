# Generated by Django 3.1.3 on 2020-11-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pracownik',
            name='numer',
            field=models.SmallIntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
