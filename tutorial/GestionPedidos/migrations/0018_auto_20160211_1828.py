# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 18:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPedidos', '0017_auto_20160211_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 18, 28, 10, 859457)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 18, 28, 10, 856989)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 18, 28, 10, 856877)),
        ),
    ]
