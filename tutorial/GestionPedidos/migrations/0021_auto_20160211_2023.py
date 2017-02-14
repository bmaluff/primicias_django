# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 20:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionClientes', '0004_cliente_direccion2'),
        ('GestionPedidos', '0020_auto_20160211_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(default=datetime.datetime(2016, 2, 11, 20, 23, 7, 535494))),
                ('direccion', models.CharField(max_length=50, null=True)),
                ('cod_pedido', models.CharField(max_length=10)),
                ('cod_det_pedido', models.CharField(max_length=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionClientes.cliente')),
            ],
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 20, 23, 7, 536451)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pago',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 20, 23, 7, 532967)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateField(default=datetime.datetime(2016, 2, 11, 20, 23, 7, 532851)),
        ),
    ]
