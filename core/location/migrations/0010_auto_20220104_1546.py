# Generated by Django 3.2.8 on 2022-01-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0009_alter_csp_lga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csp',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='csp',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcsp',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcsp',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
