# -*- coding: utf-8 -*-
from django import forms


#"""
#Este formulario es utilizado para los filtrados y busqueda
#personalizada de los platos
#existentes en la base de datos.
#"""


class Tipos_Comida_form(forms.Form):
    Busqueda = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special'}),
        required=False)


class Tipos_Postre_form(forms.Form):
    Busqueda = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special'}),
        required=False)