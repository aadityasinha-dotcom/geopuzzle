# Generated by Django 2.2.8 on 2020-01-06 04:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_auto_20190620_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='osm_data',
            new_name='_osm_data',
        ),
        migrations.AlterField(
            model_name='region',
            name='_osm_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_column='osm_data', default=dict),
        ),
    ]
