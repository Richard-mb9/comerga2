from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import form_produto_restaurante
from .forms import form_bebidas
from .models import produto_restaurante
from .models import bebidas
from produtos.models import Produtos
from cadastros.models import Lojas
from django.http import HttpResponse
from json import loads
import json
from pedidos.views import calcularTotal,verifica_qt_lojas
from cadastros.models import usuarios
from pedidos.models import SubPedido,pedidos



@login_required
def novo_produto_restaurante(req):
    form = form_produto_restaurante(req.POST or None, req.FILES or None)

    if req.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('meus_produtos_restaurante')

    return render(req,'restaurantes/form_produto_restaurante.html',{'form':form})

@login_required
def cad_bebidas(req):
    form = form_bebidas(req.POST or None, req.FILES or None)

    if req.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('meus_produtos_restaurante')

    return render(req,'restaurantes/form_bebidas.html',{'form':form})


@login_required
def restaurante(req,id):
    p = produto_restaurante.objects.filter(id_loja=id)
    b = bebidas.objects.filter(id_loja=id)

    return render(req,'restaurantes/restaurante.html',{'produtos':p,'bebidas':b})

@login_required
def Meus_produtos(req):
    u = get_object_or_404(Lojas,pk=req.user.id)
    produto = produto_restaurante.objects.filter(id_loja=u)
    b = bebidas.objects.filter(id_loja=u)

    return render(req,'restaurantes/meus_produtos.html',{'produtos':produto,'bebidas':b})


@login_required
def editar_produto(req,id):
    produto = get_object_or_404(produto_restaurante,pk=id)
    form = form_produto_restaurante(req.POST or None, req.FILES or None,instance=produto)
    if req.method == 'POST':
        if form.is_valid():
            p = get_object_or_404(Produtos,id=produto.produto.id)
            p.delete()
            form.save()
            return redirect('meus_produtos_restaurante')

    return render(req,'restaurantes/editar_produto_restaurante.html',{'form':form})


@login_required
def editar_bebidas(req,id):
    bebida = get_object_or_404(bebidas,pk=id)
    form = form_bebidas(req.POST or None, req.FILES or None,instance=bebida)

    if req.method == 'POST':
        if form.is_valid():
            p = get_object_or_404(Produtos,id=bebida.produto.id)
            p.delete()
            form.save()
            return redirect('meus_produtos_restaurante')

    return render(req,'restaurantes/editar_bebidas.html',{'form':form})

@login_required
@csrf_exempt
def excluir_produto(req):
    obj = loads(req.body)
    produto = get_object_or_404(produto_restaurante,pk=obj['id'])
    produto.delete()
    resposta = {'resposta':True}
    return HttpResponse(json.dumps(resposta))

@login_required
@csrf_exempt
def excluir_bebida(req):
    obj = loads(req.body)
    bebida = get_object_or_404(bebidas,pk=obj['id'])
    bebida.delete()
    resposta = {'resposta':True}
    return HttpResponse(json.dumps(resposta))

@login_required
@csrf_exempt
def adicionar_carrinho(req):
    obj = loads(req.body)
    usuario = req.user.id
    quantidade = float(obj['quantidade'])
    item = ""
    if obj['categoria'] == 'produto':
        pro = get_object_or_404(produto_restaurante, pk=obj['id'])
        item = get_object_or_404(Produtos,pk=pro.produto.id)
    if obj['categoria'] == 'bebida':
        beb = get_object_or_404(bebidas,pk=obj['id'])
        item = get_object_or_404(Produtos,pk=beb.produto.id)
    usu = get_object_or_404(usuarios, pk=usuario)
    tot = 0
    resposta = ""
    loja_diferente = False

    if usu.ultimopedido == "#":
        tot = float(quantidade)*float(item.valor)
        subped = SubPedido(Quantidade=quantidade,item=item,total=tot,loja=item.id_loja)
        subped.save()
        ped = pedidos(cliente=usu)
        ped.save()
        ped.itens.add(subped)
        usu.ultimopedido = ped.pedido
        usu.save()
        total = calcularTotal(usu.ultimopedido)
        ped.total = total
        ped.save()
        resposta = {'total':str(total),'loja_diferente':False}

    else:
        tot = float(quantidade)*float(item.valor)
        ped = get_object_or_404(pedidos,pk=usu.ultimopedido)
        
        #cria um novo Pedido caso o ultimo pedido esteja fechado
        if ped.pedidofechado == "sim":  
            loja_diferente = verifica_qt_lojas(item, ped)
            if loja_diferente == False:
                subped = SubPedido(Quantidade=quantidade,item=item,total=tot,loja=item.id_loja)
                subped.save()
                ped = pedidos(cliente=usu)
                ped.save()
                ped.itens.add(subped)
                usu.ultimopedido = ped.pedido
                usu.save()
                total = calcularTotal(usu.ultimopedido)
                ped.total = total
                ped.save()
                resposta = {'total':str(total),'loja_diferente':False}
            else:
                resposta = {'loja_diferente':True}

        #caso o ultimo pedido esteja aberto apenas vincula o subpedido a ele
        else:   
            loja_diferente = verifica_qt_lojas(item, ped)
            if loja_diferente == False:
                tot = float(quantidade)*float(item.valor)
                subped = SubPedido(Quantidade=quantidade,item=item,total=tot,loja=item.id_loja)
                subped.save()
                ped.itens.add(subped)
                total = calcularTotal(usu.ultimopedido)
                ped.total = total
                ped.save()
                resposta = {'total':str(total),'loja_diferente':False}
            else:
                resposta = {'loja_diferente':True}
    
           
    return HttpResponse(json.dumps(resposta))

    
    
