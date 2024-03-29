# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-28 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionPlatos', '0006_auto_20160128_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('comida', models.ManyToManyField(to='GestionPlatos.comida')),
                ('postre', models.ManyToManyField(to='GestionPlatos.postre')),
            ],
            options={
                'default_permissions': (),
                'permissions': (('gestion_menu', 'Gestion de Menu'), ('consultar_menu', 'Consultar Menu'), ('modificar_menu', 'Modificar Menu'), ('eliminar_menu', 'Eliminar Menu'), ('crear_menu', 'Crear Menu'), ('listar_menu', 'Listar Menu')),
            },
        ),
    ]
