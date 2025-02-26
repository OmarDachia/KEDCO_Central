# Generated by Django 3.2.8 on 2022-10-12 15:07

import core.utils.units
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_contractorprofile_historicalcontractorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractorprofile',
            name='uid',
            field=models.CharField(default=core.utils.units.genserial, max_length=10),
        ),
        migrations.AddField(
            model_name='historicalcontractorprofile',
            name='uid',
            field=models.CharField(default=core.utils.units.genserial, max_length=10),
        ),
    ]
