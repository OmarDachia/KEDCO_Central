# Generated by Django 3.2.8 on 2022-01-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0010_auto_20220104_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csp',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='historicalcsp',
            name='title',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
