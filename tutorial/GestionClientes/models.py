from __future__ import unicode_literals

from django.db import models
# Create your models here.


class cliente(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=50)
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


class direccionesXcliente(models.Model):
    direccion = models.CharField(max_length=150)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    zona = models.CharField(max_length=2)

    def __str__(self):
        return self.direccion
