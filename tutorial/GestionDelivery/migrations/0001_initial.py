# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-22 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionPedidos', '0032_auto_20160222_1106'),
        ('GestionUsuarios', '0004_auto_20160201_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='pedidoXzona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_delivery', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionUsuarios.funcionario')),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.factura')),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.detalle_pedido')),
            ],
            options={
                'default_permissions': (),
                'permissions': (('agregar_carrito', 'Agregar al Carrito'), ('eliminar_carrito', 'Eliminar del Carrito')),
            },
        ),
        migrations.CreateModel(
            name='zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionUsuarios.funcionario')),
            ],
            options={
                'default_permissions': (),
                'permissions': (('consultar_zona', 'Consulta de zona'), ('modificar_zona', 'Modificar zona'), ('eliminar_zona', 'Eliminar zona'), ('crear_zona', 'Crear zona'), ('listar_zona', 'Listar zona')),
            },
        ),
        migrations.AddField(
            model_name='pedidoxzona',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDelivery.zona'),
        ),
    ]
