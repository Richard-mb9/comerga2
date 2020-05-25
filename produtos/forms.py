from .models import Produtos
from .models import imagens_produtos
from django.forms.widgets import ClearableFileInput
from django import forms

class form_produto(forms.ModelForm):
    imagem = forms.ImageField(widget=ClearableFileInput)
    class Meta:
        model = Produtos
        fields = ['codigo_de_barras','nome','valor','produto_pesavel','imagem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_de_barras'].label = 'Codigo de Barras'
        #self.fields['id_loja'].widget.attrs.update({'class': 'invisivel'})

class form_imagem(forms.ModelForm):
    imagem = forms.ImageField(widget=ClearableFileInput)
    class Meta:
        model = imagens_produtos
        fields = ['codigo_de_barras','imagem']