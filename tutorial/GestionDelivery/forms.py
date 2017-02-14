# -*- coding: utf-8 -*-
from django import forms


class Tipos_Zona_form(forms.Form):
    Busqueda = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'special'}),
        required=False)