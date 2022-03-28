from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from datetime import datetime
from tutorial.GestionClientes.models import cliente
from tutorial.GestionPlatos.models import comida, postre

# Create your models here.


class pedido(models.Model):
    TIPO_PAGO = (
        ('D', 'Diario'),
        ('S', 'Semanal'),
        )
    cliente = models.ForeignKey(cliente)
    fecha_pedido = models.DateField()
    costo_pedido = models.CharField(max_length=10)
    factura = models.BooleanField(default=False)
    fecha_pago = models.DateField()
    tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO, default='D')
    is_pagado = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_pedido', 'Gestion de Pedido'),
            ('consultar_pedido', 'Consulta de pedido'),
            ('modificar_pedido', 'Modificar pedido'),
            ('eliminar_pedido', 'Eliminar pedido'),
            ('crear_pedido', 'Crear pedido'),
            ('listar_pedido', 'Listar pedido'),
            )


class detalle_pedido(models.Model):
    TIPO_COMIDA = (
        ('L', 'Light'),
        ('R', 'Regular'),
        ('S', 'Saludable'),
        )
    cod_pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    # comida = models.ForeignKey(comida) este el tipo de columna para el futuro
    comida = models.CharField(max_length=1, choices=TIPO_COMIDA)
    postre = models.ForeignKey(postre, null=True, blank=True)
    cantidad_comida = models.IntegerField(default=1)
    cantidad_postre = models.IntegerField(default=1)
    costo = models.CharField(max_length=10)
    fecha = models.DateField()
    is_pagado = models.BooleanField(default=False)
    direccion = models.CharField(max_length=50, null=True)
    zona = models.CharField(max_length=2, null=True)
    telefono = models.CharField(max_length=12, null=True)

    class Meta:
        default_permissions = ()
        permissions = ()


class factura(models.Model):
    cliente = models.ForeignKey(cliente)
    fecha_pago = models.DateField()
    direccion = models.CharField(max_length=50, null=True)
    zona = models.CharField(max_length=2, null=True)
    telefono = models.CharField(max_length=12, null=True)
    cod_pedido = models.CharField(max_length=10)
    cod_det_pedido = models.CharField(max_length=10)

    class Meta:
        default_permissions = ()
        permissions = ()


class pago(models.Model):
    cliente = models.ForeignKey(cliente)
    fecha_pago = models.DateField()
    cod_pedido = models.CharField(max_length=10)
    cod_det_pedido = models.CharField(max_length=10)
    fecha_carga = models.DateField(default=timezone.now)

    class Meta:
        default_permissions = ()
        permissions = ()
