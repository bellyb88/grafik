# Generated by Django 3.1.3 on 2020-11-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20201123_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zmiana',
            name='nazwa',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]