# Generated by Django 3.2.8 on 2022-01-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gridx', '0004_auto_20220104_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltransformer',
            name='capacity',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='historicaltransformer',
            name='ratio',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transformer',
            name='capacity',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transformer',
            name='ratio',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransformer',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicaltransformer',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='transformer',
            name='billing_postpaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='transformer',
            name='billing_prepaid_id',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
