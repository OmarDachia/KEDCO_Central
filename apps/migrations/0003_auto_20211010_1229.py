# Generated by Django 3.2.8 on 2021-10-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_historicalapplication_historicaluserappprivilege'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalapplication',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='historicaluserappprivilege',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
    ]
