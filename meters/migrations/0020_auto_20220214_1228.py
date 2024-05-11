# Generated by Django 3.2.8 on 2022-02-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0019_auto_20220204_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmeterapplication',
            name='request_type',
            field=models.CharField(choices=[('new', 'New'), ('existing', 'existing'), ('separation', 'Separation'), ('replacement', 'Replacement')], default='new_request', max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalmeterapplicationkyc',
            name='customer_type',
            field=models.CharField(choices=[('new', 'New'), ('existing', 'existing'), ('separation', 'Separation'), ('replacement', 'Replacement')], default='new', max_length=15),
        ),
        migrations.AlterField(
            model_name='meterapplication',
            name='request_type',
            field=models.CharField(choices=[('new', 'New'), ('existing', 'existing'), ('separation', 'Separation'), ('replacement', 'Replacement')], default='new_request', max_length=20),
        ),
        migrations.AlterField(
            model_name='meterapplicationkyc',
            name='customer_type',
            field=models.CharField(choices=[('new', 'New'), ('existing', 'existing'), ('separation', 'Separation'), ('replacement', 'Replacement')], default='new', max_length=15),
        ),
    ]
