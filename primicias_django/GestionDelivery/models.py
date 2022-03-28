from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from tutorial.GestionClientes.models import cliente
from tutorial.GestionPedidos.models import detalle_pedido, factura
from tutorial.GestionUsuarios.models import funcionario
# Create your models here.


class zona(models.Model):
    nombre = models.CharField(max_length=30)
    encargado = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_zona', 'Gestion de zona'),
            ('consultar_zona', 'Consulta de zona'),
            ('modificar_zona', 'Modificar zona'),
            ('eliminar_zona', 'Eliminar zona'),
            ('crear_zona', 'Crear zona'),
            ('listar_zona', 'Listar zona'),
            )


class pedidoXzona(models.Model):
    fecha_delivery = models.DateField()
    zona = models.ForeignKey(zona)
    delivery = models.ForeignKey(funcionario)
    pedido = models.ForeignKey(detalle_pedido, null=True, blank=True)
    factura = models.ForeignKey(factura, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        permissions = (
            ('agregar_carrito', 'Agregar al Carrito'),
            ('eliminar_carrito', 'Eliminar del Carrito'),
            )
