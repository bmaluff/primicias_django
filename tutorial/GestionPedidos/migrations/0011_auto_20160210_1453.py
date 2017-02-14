# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 14:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPedidos', '0010_auto_20160210_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='factura',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 10, 14, 53, 4, 829708)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 10, 14, 53, 4, 827212)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateField(default=datetime.datetime(2016, 2, 10, 14, 53, 4, 827096)),
        ),
    ]
