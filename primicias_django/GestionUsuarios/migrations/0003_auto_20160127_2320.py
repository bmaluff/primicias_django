# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 23:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestionUsuarios', '0002_auto_20160120_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_pedido',
            name='cod_comida',
        ),
        migrations.RemoveField(
            model_name='detalle_pedido',
            name='cod_pedido',
        ),
        migrations.DeleteModel(
            name='comida',
        ),
        migrations.DeleteModel(
            name='detalle_pedido',
        ),
    ]
