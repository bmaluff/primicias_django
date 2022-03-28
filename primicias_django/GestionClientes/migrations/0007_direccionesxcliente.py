# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-18 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionClientes', '0006_auto_20170218_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='direccionesXcliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=150)),
                ('zona', models.CharField(max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionClientes.cliente')),
            ],
        ),
    ]