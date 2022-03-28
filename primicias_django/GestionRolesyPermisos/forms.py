# -*- coding: utf-8 -*-
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.auth.models import Permission, Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from django import forms


class RolForm(ModelForm):

    permissions = ModelMultipleChoiceField(
        queryset=Permission.objects.filter(~Q(content_type=1),
            ~Q(content_type=2), ~Q(content_type=3), ~Q(content_type=4),
            ~Q(content_type=5), ~Q(content_type=6)),
                label=('Seleccionar permisos'),
                widget=FilteredSelectMultiple('Permisos',
                    is_stacked=False), help_text='',)

    """
    Formulario para la creacion de roles
    Hereda de forms.ModelForm y utiliza la clase Group para
    agregar ciertos campos a la hora de la creacion/modificacion/eliminacion
    """

    class Meta:
        model = Group

        fields = ['name', 'permissions']

        labels = {
            'name': ('Bader'),
        }


class RolFormBader2(ModelForm):
    OPCIONES = []
    for e in Permission.objects.filter(~Q(content_type=1),
    ~Q(content_type=2), ~Q(content_type=3), ~Q(content_type=4),
    ~Q(content_type=5), ~Q(content_type=6)):
        opt = [int(e.id), str(e.name)]
        OPCIONES.append(opt)
    OPT = ['1', '2', '3']

    permissions = forms.MultipleChoiceField(choices=OPCIONES,
    label='Seleccione los Permisos')
    name = forms.CharField(label='Nombre del Rol')

    class Meta:

        model = Group
        fields = ['name', 'permissions']


class Busqueda_Rol_form(forms.Form):

    Busqueda = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'special'}), required=False,)