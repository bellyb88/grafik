# Generated by Django 3.1.3 on 2020-12-08 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0028_pracownik_dni_urlopu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosba',
            name='pracownik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prosby', to='generator.pracownik'),
        ),
        migrations.AlterField(
            model_name='urlop',
            name='pracownik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urlopy', to='generator.pracownik'),
        ),
    ]
