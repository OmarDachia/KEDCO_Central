# Generated by Django 3.2.8 on 2021-12-17 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211216_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluserprofile',
            name='user_type',
            field=models.CharField(choices=[('technical_staff', 'Technical Staff'), ('non_technical_staff', 'Non Technical Staff'), ('nysc', 'NYSC')], default='technical_staff', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('technical_staff', 'Technical Staff'), ('non_technical_staff', 'Non Technical Staff'), ('nysc', 'NYSC')], default='technical_staff', max_length=20),
        ),
    ]
