# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20161104_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='current_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='difference',
            field=models.IntegerField(null=True),
        ),
    ]
