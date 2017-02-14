# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionClientes', '0002_cliente_ruc_ci'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'default_permissions': (), 'permissions': (('consulta_cliente', 'Consulta de Cliente'), ('modificar_cliente', 'Modificar Cliente'), ('eliminar_cliente', 'Eliminar Cliente'), ('crear_cliente', 'Crear Cliente'), ('listar_cliente', 'Listar Cliente'))},
        ),
        migrations.AddField(
            model_name='cliente',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
