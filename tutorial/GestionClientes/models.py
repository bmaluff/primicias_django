from __future__ import unicode_literals

from django.db import models
# Create your models here.


class cliente(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    zona1 = models.CharField(max_length=3, null=True)
    direccion2 = models.CharField(max_length=150, blank=True)
    zona2 = models.CharField(max_length=3, null=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=12)
    telefono_2 = models.CharField(max_length=12, blank=True)
    ruc_ci = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_cliente', 'Gestion de Cliente'),
            ('consulta_cliente', 'Consulta de Cliente'),
            ('modificar_cliente', 'Modificar Cliente'),
            ('eliminar_cliente', 'Eliminar Cliente'),
            ('crear_cliente', 'Crear Cliente'),
            ('listar_cliente', 'Listar Cliente'),
            )
