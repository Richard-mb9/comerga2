from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from django import forms
from .models import usuarios
from .models import Lojas
from .models import enderecos
from .models import arquivos
from .models import horarios
from .models import problemas

class form_usuarios(ModelForm):
    senha =  forms.CharField(widget=forms.PasswordInput) 
    confirm = forms.CharField(widget=forms.PasswordInput) 
    class Meta:
        model = usuarios
        fields = ['Primeiro_nome','Ultimo_nome' ,'email','senha','confirm','DDD_tel','telefone','DDD_cel','celular']


class form_loja(forms.ModelForm):
    senha =  forms.CharField(widget=forms.PasswordInput) 
    confirm = forms.CharField(widget=forms.PasswordInput) 
    logomarca = forms.ImageField(widget=ClearableFileInput)
    class Meta:
        model = Lojas
        fields = [
            'nome','CNPJ',
            'email','senha',
            'confirm','DDD_tel',
            'Telefone','DDD_whats',
            'whatsapp','ativa',
            'distancia','CEP',
            'Estado','Cidade',
            'bairro','Rua',
            'numero','complemento',
            'categoria',
            'Banco',
            'agencia','digito_agencia',
            'conta','digito_conta',
            'valor_minimo_compra',
            'valor_minimo_frete',
            'valor_frete','logomarca'
            ]
        #fields = '__all__'

    #função para dar atributos aos itens em html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logomarca'].widget.attrs.update({'id': 'input_logomarca'})
    

class form_endereco(forms.ModelForm):
    class Meta:
        model =enderecos
        fields = ['cliente','CEP','Estado','Cidade','bairro','Rua','numero','complemento']

class form_arquivos(forms.ModelForm):
    arquivo = forms.FileField(widget=ClearableFileInput)
    class Meta:
        model = arquivos
        fields = ['cliente','arquivo']

class form_horarios(forms.ModelForm):
    class Meta:
        model = horarios
        fields = [
            'seg_abre','seg_fecha',
            'ter_abre','ter_fecha',
            'qua_abre','qua_fecha',
            'qui_abre','qui_fecha',
            'sex_abre','sex_fecha',
            'sab_abre','sab_fecha',
            'dom_abre','dom_fecha',
        ]

class form_Problema(forms.ModelForm):
    class Meta:
        model = problemas
        fields = ['Email','Telefone','Mensagem']