from __future__ import unicode_literals

from django.db import models

# Create your models here.


class comida(models.Model):
    TIPO_COMIDA = (
        ('LIGHT', 'Light'),
        ('REGULAR', 'Regular'),
        ('SALUDABLE', 'Saludable'),
        )
    nombre = models.CharField(max_length=100)
    calorias = models.CharField(max_length=10, choices=TIPO_COMIDA)
    precio = models.CharField(max_length=10, default=15000)
    is_active = models.BooleanField(default=True)

    class Meta:
            default_permissions = ()
            permissions = (
                ('gestion_comidas', 'Gestion de Comidas'),
                ('consultar_comida', 'Consultar Comida'),
                ('modificar_comida', 'Modificar Comida'),
                ('eliminar_comida', 'Eliminar Comida'),
                ('crear_comida', 'Crear Comida'),
                ('listar_comida', 'Listar Comida'),
                )


class postre(models.Model):
    TIPO_COMIDA = (
        ('LIGHT', 'Light'),
        ('REGULAR', 'Regular'),
        ('SALUDABLE', 'Saludable'),
        )
    nombre = models.CharField(max_length=100)
    calorias = models.CharField(max_length=10, choices=TIPO_COMIDA)
    precio = models.CharField(max_length=10, default=15000)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        permissions = (
                ('gestion_postres', 'Gestion de Postres'),
                ('consultar_postre', 'Consultar Postre'),
                ('modificar_postre', 'Modificar Postre'),
                ('eliminar_postre', 'Eliminar Postre'),
                ('crear_postre', 'Crear Postre'),
                ('listar_postres', 'Listar Postres'),
                )