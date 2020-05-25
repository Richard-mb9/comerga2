from django import template
from cadastros.models import Lojas
from cadastros.models import usuarios
from produtos.models import imagens_produtos
from produtos.models import Produtos
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from pedidos.models import pedidos
from pedidos.models import SubPedido
from cadastros.models import Lojas

register = template.Library()


@register.simple_tag
def is_loja(username):
    #Verifica se o usuario logado é uma loja ou não
    is_Loja = False
    try:
        u = Lojas.objects.get(email=username)
        if u:
            is_Loja = True
    except:
        try:
            u = usuarios.objects.get(email=username)
            if u == 1:
                is_Loja = False
        except:
            pass
    
    return is_Loja



@register.simple_tag
def img_produto(produto):
    """
    Verifica se o produto possui imagem cadastrada,
    caso não possua verifica se existe alguma imagem
    cadastrada em nosso banco de dados com o mesmo
    codigo de barras, e retorna a imagem,
    caso não há nehuma imagem em nenhum dos dois casos
    retorna a string 'vazio'!
    """
    p = get_object_or_404(Produtos,pk=produto)

    if p.imagem != '#':
        return p.imagem
    else:
        pro = imagens_produtos.objects.filter(codigo_de_barras=p.codigo_de_barras)
        if len(pro) == 1:
            i = pro[0]
            return i.imagem
        else:
            return "vazio"

@register.simple_tag
def is_admin(username):
    u = get_object_or_404(User, username=username)
    grupo = ""
    try:
        grupo = u.groups.all()
        if grupo[0].name == "Administração":
            return "Administração"
    except:
        return 'vazio'


#recebe o numero do pedido re retorna a qual loja ele pertence
@register.simple_tag
def loja(pedido):
    sub = SubPedido.objects.filter(pedidos__pk=pedido)
    if sub:
        loja = sub[0].item.id_loja
        return loja
    else:
        return 'pedido vazio'



@register.simple_tag
def categoria(categoria):
    if categoria == "Restaurantes" or categoria == "Lanchonetes" or categoria == "Pizzarias":
        return "comida"
    else:
        return "não"
    
