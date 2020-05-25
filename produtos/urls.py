from django.urls import path
from .views import novoProduto
from .views import produtosCadastrados
from .views import vender
from .views import excluir_produto
from .views import editar_produto



urlpatterns = [
    path('novo-produto/',novoProduto, name='novo-produto'),
    path('produtos-cadastrados/<int:id>/',produtosCadastrados,name='produtos-cadastrados'),
    path('vender/', vender,name='vender'),
    path('exluir-produto/',excluir_produto,name='excluir_produto'),
    path('editar-produto/<int:id>/',editar_produto,name='editar_produto'),

]