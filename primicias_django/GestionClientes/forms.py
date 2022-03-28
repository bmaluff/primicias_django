# -*- coding: utf-8 -*-
from django import forms


# """
# Este formulario es utilizado para los filtrados y busqueda
# personalizada de los clientes
# existentes en la base de datos.
# """


class Tipos_Usuario_form(forms.Form):
    Busqueda = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special'}),
        required=False)
