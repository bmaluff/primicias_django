# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-25 22:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionClientes', '0004_cliente_direccion2'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='zona1',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='zona2',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
