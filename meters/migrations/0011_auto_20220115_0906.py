# Generated by Django 3.2.8 on 2022-01-15 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0010_auto_20220109_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeterapplicationinstallation',
            name='seal_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='historicalmeterapplicationpayment',
            name='mode_of_payment',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='meterapplicationinstallation',
            name='seal_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='meterapplicationpayment',
            name='mode_of_payment',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
