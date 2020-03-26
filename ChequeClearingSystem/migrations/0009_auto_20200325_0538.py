# Generated by Django 3.0.4 on 2020-03-25 05:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ChequeClearingSystem', '0008_auto_20200325_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bearerbank',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
        migrations.AlterField(
            model_name='bearerbankcheque',
            name='timeDeposited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payeebank',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
        migrations.AlterField(
            model_name='payeebankcheque',
            name='timeDeposited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]