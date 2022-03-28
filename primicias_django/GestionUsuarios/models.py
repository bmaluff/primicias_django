

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class funcionario(User):
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=12)
    telefono_2 = models.CharField(max_length=12, blank=True, null=True)
    salario = models.FloatField(default=1900000, blank=True)

    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_usuario', 'Gestion de Usuario'),
            ('consulta_usuario', 'Consultar Usuarios'),
            ('modificar_usuario', 'Modificar Usuarios'),
            ('eliminar_usuario', 'Eliminar Usuarios'),
            ('crear_usuario', 'Crear Usuarios'),
            ('listar_usuario', 'Listar Usuarios'),
            )


#class pedido(models.Model):
#    cod_cliente = models.ForeignKey(cliente)
#    cantidad = models.IntegerField()
#    costo = models.FloatField()

    #class Meta:
#            default_permissions = ()
#            permissions = ()


#class detalle_pedido(models.Model):
#    cod_pedido = models.ForeignKey(pedido)
#    cod_comida = models.ManyToManyField(comida)

#    class Meta:
#            default_permissions = ()
#            permissions = ()