# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-17 20:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPedidos', '0024_auto_20160212_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='fecha_carga',
            field=models.DateField(default=datetime.datetime(2016, 2, 17, 20, 11, 39, 942943)),
        ),
    ]