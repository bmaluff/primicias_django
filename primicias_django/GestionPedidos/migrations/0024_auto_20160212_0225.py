# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-12 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPedidos', '0023_auto_20160212_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha_pago',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pago',
            field=models.DateField(),
        ),
    ]
