# Generated by Django 3.2.8 on 2022-02-01 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0016_auto_20220131_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmeterapplicationinstallation',
            name='FPU',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='historicalmeterapplicationinstallation',
            name='SGC',
            field=models.PositiveIntegerField(default=999962, help_text='Vendor OLD SGC'),
        ),
        migrations.AlterField(
            model_name='meterapplicationinstallation',
            name='FPU',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='meterapplicationinstallation',
            name='SGC',
            field=models.PositiveIntegerField(default=999962, help_text='Vendor OLD SGC'),
        ),
    ]
