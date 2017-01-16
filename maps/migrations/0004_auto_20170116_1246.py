# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_country_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='infobox',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.CharField(db_index=True, max_length=15),
        ),
    ]
