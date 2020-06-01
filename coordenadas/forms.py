from django.forms import ModelForm
from .models import solicitacoes_geo

class form_solicitacoes(ModelForm):
    class Meta:
        model = solicitacoes_geo
        fields = ['data','hora','ender']