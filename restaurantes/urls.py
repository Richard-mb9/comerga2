from django.urls import path
from .views import novo_produto_restaurante
from .views import restaurante
from .views import cad_bebidas
from .views import Meus_produtos
from .views import excluir_produto
from .views import editar_produto
from .views import editar_bebidas
from .views import excluir_bebida
from .views import adicionar_carrinho
from django.conf.urls.static import static
from comerga import settings

urlpatterns = [
    path('novo-produto-restaurante/',novo_produto_restaurante,name='cad_prod_restaurante'),
    path('restaurante/<int:id>/',restaurante,name='restaurante'),
    path('cad-bebida/',cad_bebidas,name='cad_bebida'),
    path('restaurante/meus-produtos/',Meus_produtos,name='meus_produtos_restaurante'),
    path('excluir-produto',excluir_produto,name='excluir_produto_restaurante'),
    path('editar-produto_restaurante/<int:id>/',editar_produto,name='editar_produto_restaurante'),
    path('editar-bebidas/<int:id>/',editar_bebidas,name='editar_bebida'),
    path('excluir-bebida/',excluir_bebida,name='excluir_bebida'),
    path('adicionar-carrinho-restaurante',adicionar_carrinho,name='adicionar_carrinho_retaurante')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)