# Generated by Django 3.2.8 on 2024-02-27 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gridx', '0008_auto_20230803_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='transmissionstation',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transmissionstation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='historicaltransmissionstation',
            name='timestamp',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaltransmissionstation',
            name='updated',
            field=models.DateTimeField(blank=True, editable=False),
        ),
    ]
