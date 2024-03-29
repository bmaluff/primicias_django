# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-12 02:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPedidos', '0022_auto_20160211_2110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'default_permissions': (), 'permissions': (('consultar_pedido', 'Consulta de pedido'), ('modificar_pedido', 'Modificar pedido'), ('eliminar_pedido', 'Eliminar pedido'), ('crear_pedido', 'Crear pedido'), ('listar_pedido', 'Listar pedido'))},
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 12, 2, 23, 58, 651596)),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 12, 2, 23, 58, 652570)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 12, 2, 23, 58, 649025)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateField(),
        ),
    ]
