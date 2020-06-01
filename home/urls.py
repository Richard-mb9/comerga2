from django.urls import path
from .views import index
from .views import home
from .views import pesquisa_home
#from .views import loja
from .views import verifica_loja
#from .views import home_categoria
from .views import pesquisa_categorias
from .views import apresentacao
from .views import Lancamento
from pedidos.views import calculo_pedido
from .listview import lista
from .listview import loja
from .listview import categoria
from .listview import home as inicio
from cadastros.models import Lojas



urlpatterns = [
    path('',index,name='home'),
    #path('inicio/<int:page>/',home,name='index'),
    path('pesquisa/<str:pesquisa>/<int:page>/',pesquisa_home,name='pesquisa_home'),
    path('loja/<int:id>/', loja.as_view(), name='loja'),
    path('verifica-loja/', verifica_loja, name='verifica_loja'),
    #path('categoria/<str:categoria>/<int:page>/',home_categoria,name='home_categoria'),
    path('pesquisa-categoria/<str:categoria>/<str:pesquisa>/<int:page>/',pesquisa_categorias,name='pesquisa_categoria'),
    path('comerga/',apresentacao,name='comerga'),
    path('comerga/aguarde/',Lancamento,name='lancamento'),
    path('lista/',lista.as_view(),name='lista'),
    path('categoria/<str:categoria>/',categoria.as_view(),name='categoria'),
    path('inicio/',inicio.as_view(),name='index'),

]