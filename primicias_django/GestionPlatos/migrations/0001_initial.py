# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('calorias', models.CharField(choices=[('LIGHT', 'Light'), ('REGULAR', 'Regular'), ('SALUDABLE', 'Saludable')], max_length=10)),
                ('precio', models.FloatField(default=15000)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('gestion_comidas', 'Gestion de Comidas'), ('consultar_comida', 'Consultar Comida'), ('modificar_comida', 'Modificar Comida'), ('eliminar_comida', 'Eliminar Comida'), ('crear_comida', 'Crear Comida'), ('listar_comida', 'Listar Comida')),
            },
        ),
        migrations.CreateModel(
            name='postre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('calorias', models.CharField(choices=[('LIGHT', 'Light'), ('REGULAR', 'Regular'), ('SALUDABLE', 'Saludable')], max_length=10)),
                ('precio', models.FloatField(default=15000)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('gestion_postres', 'Gestion de Postres'), ('consultar_postre', 'Consultar Postre'), ('modificar_postre', 'Modificar Postre'), ('eliminar_postre', 'Eliminar Postre'), ('crear_postre', 'Crear Postre'), ('listar_postres', 'Listar Postres')),
            },
        ),
    ]