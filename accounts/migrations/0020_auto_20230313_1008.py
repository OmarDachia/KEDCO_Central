# Generated by Django 3.2.8 on 2023-03-13 09:08

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20221223_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpasswordresettokens',
            name='expired_time',
            field=models.DateTimeField(default=accounts.models.dlt_expired),
        ),
        migrations.AddField(
            model_name='passwordresettokens',
            name='expired_time',
            field=models.DateTimeField(default=accounts.models.dlt_expired),
        ),
    ]
