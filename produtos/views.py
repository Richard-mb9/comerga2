from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cadastros.models import Lojas
from .forms import form_produto
from .models import Produtos
from cadastros.models import arquivos
import os
import json
from json import loads



@login_required
def novoProduto(req):
    form = form_produto(req.POST or None, req.FILES or None)
    if req.user.is_authenticated:
        p = get_object_or_404(Lojas,pk=req.user.id)
        if p.categoria.categoria == 'Restaurantes':
            return redirect('cad_prod_restaurante')
        
        if p.categoria.categoria == 'Pizzarias':
            return redirect('cad_prod_restaurante')

        if p.categoria.categoria == 'Lanchonetes':
            return redirect('cad_prod_restaurante')
        form.fields['imagem'].initial = "#"
        id = req.user.id
        loja = Lojas.objects.filter(id=id)
        if form.is_valid():
            l =form.save(commit=False)
            l.id_loja = loja[0]
            l.save()
            return redirect('produtos-cadastrados',id=id)
    return render(req ,'produtos/novo-produto.html',{'form':form})

@login_required
def produtosCadastrados(req,id):
    try:
        arq = get_object_or_404(arquivos,cliente=req.user.id) 
        os.remove("media/" + str(arq.arquivo)) 
        arq.delete()
    except:
        pass
    
    loja = get_object_or_404(Lojas,pk=id)
    if loja.categoria.categoria == 'Restaurantes':
        return redirect('meus_produtos_restaurante')
    
    if loja.categoria.categoria == 'Pizzarias':
        return redirect('meus_produtos_restaurante')

    if loja.categoria.categoria == 'Lanchonetes':
        return redirect('meus_produtos_restaurante')
    lista = Produtos.objects.filter(id_loja=id)
    return render(req,'produtos/produtos-cadastrados.html',{'lista':lista})

@login_required
def vender(req):
    loja = ""
    try:
        loja = get_object_or_404(Lojas,pk=req.user.id)
    except:
        pass
    return render(req, 'produtos/vender.html',{'loja':loja})



#deletar determinado produto
@login_required
@csrf_exempt
def excluir_produto(req):
    obj = loads(req.body)
    id = obj['id']
    produto = get_object_or_404(Produtos,pk=id)
    produto.delete()
    resposta = {'resposta':True}
    return HttpResponse(json.dumps(resposta))


@login_required
def editar_produto(req,id):
    p = get_object_or_404(Produtos,pk=id)
    form = form_produto(req.POST or None, req.FILES or None, instance=p)
    if req.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('produtos-cadastrados', req.user.id)
    return render(req, 'produtos/editar_produto.html',{'form':form})




