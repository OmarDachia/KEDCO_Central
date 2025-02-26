# Generated by Django 3.2.8 on 2022-09-27 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nmmp', '0010_auto_20220311_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='NMMPApplicationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('inactive', 'Inactive'), ('active', 'Active')], max_length=10)),
            ],
            options={
                'verbose_name': 'NMMP Application Type',
                'verbose_name_plural': 'NMMP Application Types',
                'ordering': ('-updated',),
            },
        ),
        migrations.AlterModelOptions(
            name='historicalnmmpkyc',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical NMMP KYC', 'verbose_name_plural': 'historical NMMP KYCs'},
        ),
        migrations.AlterModelOptions(
            name='historicalnmmpmeter',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical NMMP Meter', 'verbose_name_plural': 'historical NMMP Meters'},
        ),
        migrations.AlterModelOptions(
            name='historicalnmmpmeterinstallation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical NMMP Meter Installation', 'verbose_name_plural': 'historical NMMP Meter Installations'},
        ),
        migrations.AlterModelOptions(
            name='historicalnmmpmeterupload',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical NMMP Meter Upload', 'verbose_name_plural': 'historical NMMP Meter Uploads'},
        ),
        migrations.AlterField(
            model_name='historicalnmmpkyc',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalnmmpmeter',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalnmmpmeterinstallation',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalnmmpmeterupload',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.CreateModel(
            name='HistoricalNMMPApplicationType',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('note', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('inactive', 'Inactive'), ('active', 'Active')], max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical NMMP Application Type',
                'verbose_name_plural': 'historical NMMP Application Types',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
