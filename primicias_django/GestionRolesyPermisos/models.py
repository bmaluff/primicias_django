from __future__ import unicode_literals

from django.contrib.auth.models import Group

# Create your models here.


class Rol(Group):

    class Meta:

        default_permissions = ()
        permissions = (
            ('gestion_rol', 'Gestion de Roles'),
            ('consulta_rol', 'Consultar Roles'),
            ('modificar_rol', 'Modificar Roles'),
            ('eliminar_rol', 'Eliminar Roles'),
            ('crear_rol', 'Crear Roles'),
            ('listar_rol', 'Listar Roles'),
            ('listar_permiso', 'Listar Permisos'),
            )