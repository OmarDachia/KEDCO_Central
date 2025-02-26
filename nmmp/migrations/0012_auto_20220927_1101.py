# Generated by Django 3.2.8 on 2022-09-27 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nmmp', '0011_auto_20220927_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnmmpkyc',
            name='application_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nmmp.nmmpapplicationtype'),
        ),
        migrations.AddField(
            model_name='nmmpkyc',
            name='application_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='nmmpkycs', to='nmmp.nmmpapplicationtype'),
            preserve_default=False,
        ),
    ]
