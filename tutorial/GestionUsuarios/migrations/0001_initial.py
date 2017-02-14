# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-13 14:42
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=150)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('telefono', models.CharField(max_length=12)),
                ('telefono_2', models.CharField(blank=True, max_length=12)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('consulta_cliente', 'Consulta de Cliente'), ('modificar_cliente', 'Modificar Cliente'), ('eliminar_cliente', 'Eliminar Cliente'), ('crear_usuario', 'Crear Cliente'), ('listar_cliente', 'Listar Cliente')),
            },
        ),
        migrations.CreateModel(
            name='comida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[(b'LIGHT', b'Light'), (b'REGULAR', b'Regular'), (b'SALUDABLE', b'Saludable')], max_length=10)),
                ('precio', models.FloatField(default=15000)),
            ],
            options={
                'default_permissions': (),
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='detalle_pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_comida', models.ManyToManyField(to='GestionUsuarios.comida')),
            ],
            options={
                'default_permissions': (),
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='funcionario',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=150)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('telefono', models.CharField(max_length=12)),
                ('telefono_2', models.CharField(blank=True, max_length=12)),
                ('salario', models.FloatField(blank=True, default=1900000)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('gestion_usuario', 'Gestion de Usuario'), ('consulta_usuario', 'Consultar Usuarios'), ('modificar_usuario', 'Modificar Usuarios'), ('eliminar_usuario', 'Eliminar Usuarios'), ('crear_usuario', 'Crear Usuarios'), ('listar_usuario', 'Listar Usuarios')),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('costo', models.FloatField()),
                ('cod_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionUsuarios.cliente')),
            ],
            options={
                'default_permissions': (),
                'permissions': (),
            },
        ),
        migrations.AddField(
            model_name='detalle_pedido',
            name='cod_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionUsuarios.pedido'),
        ),
    ]
