from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Transferencias
from cadastros.models import Lojas
from pedidos.models import pedidos, SubPedido
from datetime import datetime,timedelta,date,time
from django.shortcuts import get_object_or_404
from comerga import settings


DIAS = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

@login_required
def Painel(req):
    #indice_semana = data.weekday()
    #dia_semana = DIAS[indice_semana]
    if req.method == "POST":
        tr = req.POST['transferencia']
        status = req.POST['status']
        print (status)
        a = get_object_or_404(Transferencias,pk=tr)
        a.status = status
        a.save()
    pg = []
    i = 0
    while (i <= 14):
        p = Transferencias.objects.filter(data=datetime.today()-timedelta(days=i))     
        if p:
            for t in p:
                pg.append(t)
        i += 1 
    for p in pg:
        p.data = p.data.strftime("%d/%m/%Y")

    return render(req,'Transferencias/Painel.html',{'pg':pg})

@login_required
def Criar_pagamentos(req):
    ped = []
    data =datetime.today()
    numero_dia_semana = data.isoweekday()
    i = numero_dia_semana
    lista_loja = []
    while (i <= 6 + numero_dia_semana ):
        p = pedidos.objects.filter(data=datetime.today()-timedelta(days=i))
        for pe in p:
            sub = SubPedido.objects.filter(pedidos__pk=pe.pedido)
            loja = sub[0].item.id_loja
            if not loja in lista_loja:
                lista_loja.append(loja)
            ped.append(pe)
        i += 1 
    for loja in lista_loja:
        total = 0
        total_frete = 0
        for p in ped:
            sub = SubPedido.objects.filter(pedidos__pk=p.pedido)
            pedido = get_object_or_404(pedidos,pedido=p.pedido)
            if sub[0].item.id_loja == loja:
                if pedido.status_pagamento == 'não pago':
                    if pedido.pedidofechado == 'sim':
                        if pedido.pedido_cancelado == 'não':
                            total += p.total
                            total_frete += p.valor_frete
                            #total += p.taxa_servico
                            pedido.status_pagamento = 'agendado'
                            pedido.save()
        if total != 0:
            total = total - ((total/100)*10)
            total += total_frete
            a = Transferencias(
                data=datetime.today(),
                loja=loja,
                Banco=loja.Banco,
                agencia=loja.agencia,
                digito_agencia=loja.digito_agencia,
                conta=loja.conta,
                digito_conta=loja.digito_conta,
                valor=total)
            a.save()
    return redirect ('painel_admin')


@login_required
def extrato(req):
    is_loja = False
    if req.user.is_authenticated:
        u = []
        try:
            u = Lojas.objects.filter(pk=req.user.id)
        except:
            pass
        if len(u) == 1:
            is_loja = True
        else:
            is_loja = False
        
        if is_loja == True:
            loja = get_object_or_404(Lojas,pk=req.user.id)
            t = Transferencias.objects.filter(loja=loja)
            for tr in t:
                tr.data = tr.data.strftime("%d/%m/%Y")
            return render(req,'Transferencias/extrato.html',{'transferencia':t})
        else:
            return redirect('home')




