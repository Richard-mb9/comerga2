from django.urls import path
from .views import novoUsuario
from .views import novoEndereco
from .views import novaLoja
from .views import criar_varios_produtos
from .views import cadastrando
from .views import meus_pedidos
from .views import meus_dados
from .views import alterar_cadastro_usuario
from .views import alterar_endereço
from .views import logar
from .views import esqueceuSenha
from .views import verifica_email


urlpatterns = [
    path('novo-usuario/',novoUsuario, name='novo-usuario'),
    path('novo-endereco/',novoEndereco,name='novo-endereco'),
    path('nova-loja/',novaLoja, name='nova-loja'),
    path('cadastrar-varios/',criar_varios_produtos, name='cadastrar-varios'),
    path('cadastrando/',cadastrando, name='cadastrando'),
    path('meus-pedidos/', meus_pedidos, name='meus_pedidos'),
    path('meus-dados/',meus_dados, name='meus_dados'),
    path('alterar-dados-cliente/',alterar_cadastro_usuario,name='alterar_dados_cliente'),
    path('alterar-endereco/' ,alterar_endereço, name='alterar_endereco'),
    path('login/', logar, name='login'),
    path('esqueceu-senha/',esqueceuSenha,name='esqueceu_senha'),
    path('verifica-email/',verifica_email,name='verifica_email')

]