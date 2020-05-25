from django.urls import path
from .views import calculo_pedido
from .views import carrinho
from .views import Excluirsubpedido
from .views import deletarsubpedido
from .views import lista_pedidos
from .views import lista_subpedidos
from .views import lista_subpedidos_cliente
from .views import limparPedido
from .views import fechar_pedido
from .views import pedido_finalizado
from .views import confirmar_endereco
from .views import alterar_endereco_pedido
from .views import salvar_endereco_pedido
from .views import pagamento_dinheiro
from .views import cancelar_pedido
from .views import imprimir_pedido



urlpatterns = [
    path('carrinho/', carrinho, name="carrinho"),
    path('addcarrinho/',calculo_pedido, name='addcarrinho'),
    path('excluir-subpedido/<int:id>/',Excluirsubpedido,name='excluir-subpedido'),
    path('deletar-subpedido/',deletarsubpedido,name='deletar-subpedido'),
    path('pedidos/',lista_pedidos, name="lista-pedidos"),
    path('pedido/<int:id>/',lista_subpedidos, name='lista-subpedidos'),
    path('pedido-cliente/<int:id>/', lista_subpedidos_cliente, name='pedido_cliente'),
    path('limpar-pedido/', limparPedido, name="limpar_pedido"),
    path('fechar-pedido/<int:pedido>/', fechar_pedido,name='fechar_pedido'),
    path('pedido_finalizado/<int:pedido>/',pedido_finalizado,name='pedido_finalizado'),
    path('confirmar-endereco/<int:pedido>/',confirmar_endereco,name='confirmar_endereco'),
    path('alterar-endereco-pedido/<int:pedido>/',alterar_endereco_pedido,name='alterar_endereco_pedido'),
    path('salvar-endereco-pedido/<int:pedido>/',salvar_endereco_pedido,name='salvar_endereco_pedido'),
    path('pagar-dinheiro/<int:pedido>/',pagamento_dinheiro,name='pagamento_dinheiro'),
    path('cancelar-pedido/<int:pedido>/',cancelar_pedido,name='cancelar_pedido'),
    path('imprimir-pedido/<int:pedido>/',imprimir_pedido,name='imprimir_pedido'),
]