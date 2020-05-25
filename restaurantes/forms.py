from django.forms import ModelForm
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import produto_restaurante
from .models import bebidas


class form_produto_restaurante(forms.ModelForm):
    foto = forms.ImageField(widget=ClearableFileInput)
    class Meta:
        model = produto_restaurante
        fields = [
            'nome',
            'id_loja',
            'descricao',
            'foto',
            'valor',
        ]

class form_bebidas(forms.ModelForm):
    foto = forms.ImageField(widget=ClearableFileInput)
    class Meta:
        model = bebidas
        fields = [
            'nome',
            'id_loja',
            'foto',
            'valor',
        ]