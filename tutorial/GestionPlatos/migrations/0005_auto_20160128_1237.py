# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-28 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPlatos', '0004_auto_20160128_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comida',
            name='precio',
            field=models.CharField(default=15000, max_length=10),
        ),
    ]
