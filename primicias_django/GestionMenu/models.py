from __future__ import unicode_literals

from django.db import models
from tutorial.GestionPlatos.models import comida, postre
# Create your models here.


class menu(models.Model):
    fecha = models.DateField(blank=False)
    comida = models.ManyToManyField(comida)
    postre = models.ManyToManyField(postre)
    is_active = models.BooleanField(default=True)

    class Meta:
            default_permissions = ()
            permissions = (
                ('gestion_menu', 'Gestion de Menu'),
                ('consultar_menu', 'Consultar Menu'),
                ('modificar_menu', 'Modificar Menu'),
                ('eliminar_menu', 'Eliminar Menu'),
                ('crear_menu', 'Crear Menu'),
                ('listar_menu', 'Listar Menu'),
                )