# Generated by Django 3.2.8 on 2022-01-31 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0015_auto_20220126_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeterapplicationinstallation',
            name='FPU',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalmeterapplicationinstallation',
            name='SGC',
            field=models.PositiveIntegerField(default=999962, help_text='Vendor OLD SGC'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meterapplicationinstallation',
            name='FPU',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meterapplicationinstallation',
            name='SGC',
            field=models.PositiveIntegerField(default=999962, help_text='Vendor OLD SGC'),
            preserve_default=False,
        ),
    ]
