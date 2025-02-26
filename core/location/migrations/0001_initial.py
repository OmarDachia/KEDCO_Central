# Generated by Django 3.2.7 on 2021-09-27 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('State_ID', models.CharField(max_length=10)),
                ('state_code', models.CharField(max_length=10)),
                ('zone', models.CharField(max_length=10)),
                ('zone_code', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LGA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('LGA_ID', models.CharField(blank=True, max_length=10, null=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.state')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
