# Generated by Django 3.2.8 on 2021-12-23 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0006_auto_20211223_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meterapplicationintallation',
            options={'ordering': ['-updated'], 'verbose_name': 'Meter Application Installation', 'verbose_name_plural': 'Meter Applications Installations'},
        ),
        migrations.AlterField(
            model_name='historicalmeterapplication',
            name='stage',
            field=models.CharField(choices=[('awaiting_kyc', 'Awaiting KYC'), ('awaiting_payment', 'Awaiting Payment'), ('awaiting_installation', 'Awaiting Installation'), ('completed', 'Completed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalmeterphase',
            name='phase',
            field=models.CharField(choices=[('single_phase', 'Single Phase'), ('two_phase', 'Two Phase'), ('three_phase', 'Three Phase'), ('md', 'MD')], max_length=15),
        ),
        migrations.AlterField(
            model_name='meterapplication',
            name='stage',
            field=models.CharField(choices=[('awaiting_kyc', 'Awaiting KYC'), ('awaiting_payment', 'Awaiting Payment'), ('awaiting_installation', 'Awaiting Installation'), ('completed', 'Completed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='meterphase',
            name='phase',
            field=models.CharField(choices=[('single_phase', 'Single Phase'), ('two_phase', 'Two Phase'), ('three_phase', 'Three Phase'), ('md', 'MD')], max_length=15),
        ),
    ]
