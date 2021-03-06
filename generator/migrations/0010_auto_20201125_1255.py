# Generated by Django 3.1.3 on 2020-11-25 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0009_auto_20201125_0704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grafik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('data_od', models.DateField(blank=True, null=True)),
                ('data_do', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='regula',
            name='dzien',
            field=models.CharField(choices=[(None, None), ('0', 'Poniedzialek'), ('1', 'Wtorek'), ('2', 'Sroda'), ('3', 'Czwartek'), ('4', 'Piatek'), ('5', 'Sobota'), ('6', 'Niedziela'), ('14', 'Pon-Pt'), ('56', 'Weekend'), ('Wszystkie', 'Wszystkie')], max_length=19),
        ),
        migrations.CreateModel(
            name='Dniowka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(db_index=True)),
                ('min_pracownicy', models.SmallIntegerField()),
                ('swieto', models.BooleanField(default=False)),
                ('pracownicy_dzien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownicy_dzien', to='generator.pracownik')),
                ('pracownicy_noc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownicy_noc', to='generator.pracownik')),
            ],
        ),
    ]
