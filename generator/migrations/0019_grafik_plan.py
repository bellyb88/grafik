# Generated by Django 3.1.3 on 2020-11-25 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0018_auto_20201125_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafik',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='generator.plan'),
            preserve_default=False,
        ),
    ]
