from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from cadastros.models import usuarios, Lojas
from cadastros.forms import form_endereco
from django.http import HttpResponse
from json import loads
import json
from .models import SubPedido
from .models import pedidos
from produtos.models import Produtos
from cadastros.models import usuarios, enderecos
from cadastros.views import busca_loja
from coordenadas.coordenadas import criarEndereco,distancia,coordenadas
from coordenadas.models import CEP
import requests
from django.http import HttpRequest
from decimal import Decimal
from datetime import datetime,timedelta
import credenciais


#calcula o saldo que uma loja tem disponivel e envia para verica_loja na app home
def calcular_saldo_loja(id):
    pedido = pedidos.objects.filter(itens__loja=id)
    total = 0
    pg_dineiro = 0
    pg_cartão = 0
    comissao = 0
    lista =  []
    for ped in pedido:
        if not ped in lista:
            lista.append(ped)
    for ped in lista:
        if ped.pedidofechado == 'sim':
            if ped.pedido_cancelado == 'não' and ped.status_pagamento == "não pago":
                total += ped.total
                if ped.forma_de_pagamento == "dinheiro":
                    pg_dineiro += ped.total
                if ped.forma_de_pagamento == "cartão":
                    pg_cartão += ped.total
    comissao = round((total/100)*10,2)
    total = total - (pg_dineiro + comissao)

    return (total)
    
    
#cria uma lista com todos os pedidos fechados da loja que esta logada
@login_required
@csrf_exempt
def lista_pedidos(req):
    ped = pedidos.objects.filter(itens__loja=req.user.id)
    lista = []
    for pedi in ped:
        if not pedi in lista:
            if pedi.pedidofechado == 'sim':
                lista.append(pedi)        
    calcular_saldo_loja(req.user.id)
    for l in lista:
        l.data = l.data.strftime("%d/%m/%Y")
    if req.method == "POST":
        obj = loads(req.body)
        pedido = get_object_or_404(pedidos,pedido=obj['id'])
        pedido.status_entrega = str(obj['status'])
        pedido.save()
    
    lista = reversed(lista)
    
    return render(req,'pedidos/lista-pedidos.html',{"pedidos":lista})

#cria uma lista de subpedidos que estão em um pedido especifico, de uma determinada loja
@login_required
def lista_subpedidos(req,id):
    sub = SubPedido.objects.filter(pedidos__pk=id)
    ped = get_object_or_404(pedidos, pedido=id)
    cliente = get_object_or_404(usuarios, pk=ped.cliente.id)
    i = cliente.id
    endereco = get_object_or_404(enderecos, cliente_id=i)
    total = ped.valor_frete + ped.taxa_servico + ped.total
    return render(req, 'pedidos/pedido.html', 
    {'subpedido':sub, 'total':total,
    'cliente':cliente,  'endereco':endereco,
    'pedido':ped})

@login_required
def imprimir_pedido(req,pedido):
    sub = SubPedido.objects.filter(pedidos__pk=pedido)
    ped = get_object_or_404(pedidos, pedido=pedido)
    cliente = get_object_or_404(usuarios, pk=ped.cliente.id)
    i = cliente.id
    endereco = get_object_or_404(enderecos, cliente_id=i)
    total = ped.valor_frete + ped.taxa_servico + ped.total
    return render(req, 'pedidos/imprimir_pedido.html', 
    {'subpedido':sub, 'total':total,
    'cliente':cliente,  'endereco':endereco,
    'pedido':ped})




@login_required
def lista_subpedidos_cliente(req,id):
    sub = SubPedido.objects.filter(pedidos__pk=id)
    ped = get_object_or_404(pedidos, pk=id)
    cliente = get_object_or_404(usuarios, pk=ped.cliente.id)
    loja = sub[0].item.id_loja
    i = cliente.id
    endereco = get_object_or_404(enderecos, cliente_id=i)

    return render(req, 'pedidos/pedido_cliente.html', 
    {'subpedido':sub,'cliente':cliente, 'pedido':ped, 'endereco':endereco,'loja':loja})



#cria uma lista de subpedidos em determinado pedido (carrinho de compras)
@login_required
def carrinho(req):
    usu = get_object_or_404(usuarios,pk=req.user.id)
    itens = ""
    if usu.ultimopedido != "#":
        ped = get_object_or_404(pedidos, pk=usu.ultimopedido)
        itens = SubPedido.objects.filter(pedidos__pk=usu.ultimopedido)
        total = ped.total
        lista = []     
        pode_comprar = ""
        for item in itens:
            if item.item.id_loja in lista:
                pass
            else:
                lista.append(item.item.id_loja)
        
        if len(lista) == 0:
            itens = "vazio"
        
        loja = ""
        if itens != "vazio":
            loja = itens[0].loja
            valor_minimo_compra = loja.valor_minimo_compra
            if valor_minimo_compra < total:
                pode_comprar = "não"
            else:
                pode_comprar = "sim"

        print("A quantidade de Lojas é: " + str(len(lista)))
    
    if usu.ultimopedido == "#":
        itens = "vazio"
        return render(req, 'pedidos/carrinho.html',{'pedido':itens})

    return render(req, 'pedidos/carrinho.html',
    {'pedido':itens, 'total':total, 'ped':ped,'loja':loja, 'pode_comprar':pode_comprar})

@login_required
@csrf_exempt
def fechar_pedido(req,pedido):
    is_loja = busca_loja(req.user.username)
    ped = pedidos.objects.get(pedido=pedido)
    itens = SubPedido.objects.filter(pedidos__pk=pedido)
    loja = itens[0].loja
    total = ped.total + ped.valor_frete + loja.categoria.taxa_servico
    

    #caso o cliente tenha escolhido a forma de pagamento em dinheiro
    if req.method == "POST":
        usu = get_object_or_404(usuarios,pk=req.user.id)
        usu.ultimopedido = "#"
        usu.save()
        resposta = {'resposta':False}
        obj = loads(req.body)
        ped.forma_de_pagamento = str(obj['forma'])
        ped.taxa_servico = loja.categoria.taxa_servico
        ped.pedidofechado = "sim"
        ped.data = datetime.today()
        ped.save()
        resposta = {'resposta':True}
        return HttpResponse(json.dumps(resposta))

    if is_loja == False and not req.method =='POST':
        ped = get_object_or_404(pedidos,pedido=pedido)
        return render(req,'pedidos/pagamento.html',
        {'ped':ped, 'pedido':pedido, 'loja':loja, 'total':total})
        
    

@login_required
def pedido_finalizado(req, pedido):
    ped = pedidos.objects.get(pedido=pedido)
    itens = SubPedido.objects.filter(pedidos__pk=pedido)
    loja = itens[0].loja
    return render(req,'pedidos/pedido_finalizado.html',
    {'pedido':ped, 'loja':loja})





#exlui o subpedido da lista 
@login_required
def Excluirsubpedido(req,id):
    sub = get_object_or_404(SubPedido,pk=id)
    sub.delete()
    return redirect('carrinho')


#deleta o subpedido sem recarregar a pagina e atualiza o valor do carrinho
@csrf_exempt
def deletarsubpedido(req):
    usu = get_object_or_404(usuarios,pk=req.user.id)
    obj = loads(req.body)
    id = int(obj['id'])
    sub = get_object_or_404(SubPedido,pk=id)
    sub.delete()
    total = str(calcularTotal(usu.ultimopedido)) 
    resposta = {'resposta':True,
    'total':total}
    return HttpResponse(json.dumps(resposta))


#apaga todos os subpedidos de um pedido
def limparPedido(req):
    usu = get_object_or_404(usuarios, pk=req.user.id)
    ped = get_object_or_404(pedidos,pk=usu.ultimopedido)
    itens = ped.itens.all()
    resposta = False
    for item in itens:
        item.delete()
        resposta = {'resposta':True}
    return HttpResponse(json.dumps(resposta))


#calcula o total do carrinho toda vez que o usuario efetua uma compra
def calcularTotal(n):
    ped = get_object_or_404(pedidos,pk=n)
    itens = ped.itens.all()
    tot = 0
    for item in itens:
        tot += item.total
    ped.total = tot
    ped.save()

    return(tot)


#calcula o total do carrinho toda vez que o usuario carrega uma pagina
def TotalCarrinho(u):
    tot = 0
    usu = get_object_or_404(usuarios,pk=u)
    if usu.ultimopedido != "#":
        ped = get_object_or_404(pedidos,pedido=usu.ultimopedido)
        itens = ped.itens.all()
        for item in itens:
            tot += item.total

    return (tot)
  

#cria e salva os subpedidos, e os adiciona no ultimo pedido ou cria um novo pedido
@csrf_exempt
def calculo_pedido(req):
    obj = loads(req.body)
    #usuario = int(obj['user'])
    usuario = req.user.id
    quantidade = float(obj['quantidade'])
    item = get_object_or_404(Produtos, pk=obj['id'])
    usu = get_object_or_404(usuarios, pk=usuario)
    tot = 0
    resposta = ""
    loja_diferente = False
    
    #caso o cliente não possua nenhum pedido aberto
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

""" Veirifica se a loja que o cliente esta efetuando a compra é a mesma
da que ja esta no pedido, caso ele esteja comprando em uma loja diferente
retorna verdadeiro"""
def verifica_qt_lojas(item, ped):
        i = ped.itens.all()
        dif = False
        for it in i:
            if item.id_loja != it.loja:
                dif = True
        return dif

@login_required
def confirmar_endereco(req,pedido):
    ender = get_object_or_404(enderecos, cliente=req.user.id)
    usu = get_object_or_404(usuarios,pk = req.user.id)
    ped = get_object_or_404(pedidos,pedido=pedido)
    obs = ""
    if ped.observacao:
        obs = ped.observacao

    if req.method == 'POST':
        ped.observacao = req.POST['obs']
        ped.save()
        obs = ped.observacao
        return render(req,'pedidos/confirmar_endereco.html',{'ender':ender, 
        'usuario':usu, 'pedido':ped,'obs':obs})

    return render(req,'pedidos/confirmar_endereco.html',{'ender':ender, 
    'usuario':usu, 'pedido':ped, 'obs':obs})

def calcular_frete(valor_frete,end1,end2):
    """end1 e end2 são dois ceps que dever ser enviados 
    para ser calculada a distancia entre os dois"""
    c1 = end1
    c2 = end2
    CEP1 = CEP.objects.filter(CEP=c1)
    CEP2 = CEP.objects.filter(CEP=c2)
    coord1 = ""
    coord2 = ""
    dis = 0
    if len(CEP1) == 1:
        CEP1 = get_object_or_404(CEP,CEP=c1)
        CEP2 = get_object_or_404(CEP,CEP=c2)
        coord1 = CEP1.Coordenadas
        coord2 = CEP2.Coordenadas
    else:
        Salvou = False
        i = 0
        while(Salvou == False or i < 10):
            try:
                e1 = criarEndereco(c1)
                e2 = criarEndereco(c2)
                coord1 = coordenadas(e1)
                coord2 = coordenadas(e2)
                salvar_CEP1 = CEP(CEP=c1,Coordenadas=coord1,endereco=e1)
                salvar_CEP2 = CEP(CEP=c2,Coordenadas=coord2,endereco=e2)
                salvar_CEP1.save()
                salvar_CEP2.save()
                Salvou = True
            except:
                Salvou = False
                i = i + 1

    #API google matrix para calcular a distancia em KMs
    calculou = False
    teste = 0
    while(calculou == False and teste <= 10):
        try:
            key = credenciais.KEY_API_GOOGLE
            r = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?units=kilometers&origins={str(coord1)}&destinations={str(coord2)}&key={key}")
            d = float(r.json()['rows'][0]['elements'][0]['distance']['value'])
            dis = float(d/1000)
            calculou = True
        except:
            teste += 1 
            print("teste = " + str(teste))
            calculou = False

    frete = (float(dis)* float(valor_frete))
    #caso não consiga calcular a distancia utilizando a api google Matrix, retornara uma string erro
    if dis == 0 and calculou == False:
        return "erro"
    return frete



#Salva o endereço que esta cadastrado pelo cliente e o adiciona ao pedido
@login_required
def salvar_endereco_pedido(req,pedido):
    ender = get_object_or_404(enderecos, cliente=req.user.id)
    sub = SubPedido.objects.filter(pedidos__pk=pedido)
    ped = get_object_or_404(pedidos,pedido=pedido)
    CEP1 = sub[0].loja.CEP
    CEP2 = ender.CEP
    frete = sub[0].loja.valor_frete
    v = calcular_frete(frete,CEP1,CEP2)
    if v == "erro":
        return HttpResponse("Tivemos um problema, infelizmente não conseguimos calcular a disntancia até a sua casa" +
        " Pedimos desculpas pelo Transtorno, por favor tente novamente dentro de 5 minutos, se o problema continuar, entre em contato conosco")
    #verifica se o valor do frete é menor do que o valor minimo do frete da loja
    if v < sub[0].loja.valor_minimo_frete:
        ped.valor_frete = sub[0].loja.valor_minimo_frete
    else:
        ped.valor_frete = v
    ped.Rua = ender.Rua
    ped.CEP = ender.CEP
    ped.numero = ender.numero
    ped.complemento = ender.complemento
    ped.Cidade = ender.Cidade
    ped.Estado = ender.Estado
    ped.save()

    return redirect('fechar_pedido', pedido)



@login_required
def alterar_endereco_pedido(req,pedido):
    usu = get_object_or_404(usuarios, pk=req.user.id)
    ender = get_object_or_404(enderecos,cliente=usu)
    form = form_endereco(req.POST or None, instance=ender)

    if req.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('confirmar_endereco', pedido)

    return render(req, 'pedidos/alterar_endereco_pedido.html', {'form':form, 'usuario':usu})


@login_required
def pagamento_dinheiro(req,pedido):
    ped = get_object_or_404(pedidos,pedido=pedido)
    itens = SubPedido.objects.filter(pedidos__pk=pedido)
    loja = itens[0].loja
    total = ped.total + ped.valor_frete + loja.categoria.taxa_servico
    if req.method == 'POST':
        precisa_troco = req.POST['precisa_troco']
        valor_troco = req.POST['valor_troco']
        if precisa_troco == 'Não':
            ped.troco = 'não'
            ped.valor_troco = 'não'
            ped.save()
            return redirect('pedido_finalizado',ped)
        else:
            ped.troco = 'Sim'
            ped.valor_troco = "R$" + str(valor_troco)
            ped.save()
            return redirect('pedido_finalizado',ped)
    
    return render(req,'pedidos/pagamento_dinheiro.html',
    {'pedido':ped,'total':total})



@login_required
def cancelar_pedido(req,pedido):
    ped = get_object_or_404(pedidos,pedido=pedido)
    if req.method == 'POST':
        print(pedido)
        motivo = req.POST['motivo_cancelamento']
        ped.motivo_cancelamento = motivo
        ped.pedido_cancelado = "sim" 
        ped.save()
        return redirect('lista-subpedidos',pedido)
        
    return render(req,'pedidos/cancelar_pedido_loja.html',{'pedido':ped})





