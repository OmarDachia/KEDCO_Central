# Generated by Django 3.2.8 on 2022-12-20 13:20

import accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20221012_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractorprofile',
            name='nemsa_licence',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(14), accounts.models.validate_contractor_nimsa]),
        ),
        migrations.AlterField(
            model_name='historicalcontractorprofile',
            name='nemsa_licence',
            field=models.CharField(db_index=True, max_length=15, validators=[django.core.validators.MinLengthValidator(14), accounts.models.validate_contractor_nimsa]),
        ),
    ]
