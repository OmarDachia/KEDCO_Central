# Generated by Django 3.2.8 on 2022-01-04 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_auto_20220104_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalregion',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalregion',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
