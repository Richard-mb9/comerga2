from django.shortcuts import render,get_list_or_404,get_list_or_404
from django.http import HttpResponse,JsonResponse

from produtos.models import Produtos
from cadastros.models import Lojas
from pedidos.models import SubPedido
from pedidos.models import pedidos
from cadastros.models import usuarios
from cadastros.models import enderecos
from cadastros.models import categorias_lojas
from coordenadas.coordenadas import criarLista
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator
from json import loads
import json
from django.views.decorators.csrf import csrf_exempt



class home(ListView):
    model = Lojas
    paginate_by = 3
    context_object_name = 'lojas'
    template_name = 'home/testes/inicio.html'
    ordering = ['nome']
    
    def get_queryset(self):
        lojas = ""
        cat = ""
        if self.request.user.is_authenticated:
            try:
                """
                Tenta filtrar quais lojas entregam em sua residencia,
                caso não consiga filtrar retornara todas as lojas cadastras no site
                """  
                u = usuarios.objects.get(id=self.request.user.id)
                end = enderecos.objects.get(cliente=u)
                c = end.CEP
                x = criarLista(c)
                lojas = x
                
            except:
                """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
                ira retornar todas as lojas cadastradas"""
                lojas = Lojas.objects.all()
        else:
            lojas = Lojas.objects.all()

        try:
            if self.request.GET['pesquisa']:
                import re
                import unidecode
                p = self.request.GET['pesquisa']
                l = []
                lista = lojas
                for item in lista:
                    encontrou = False
                    if re.search(str(p),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                        l.append(item)
                        encontrou = True
                    if re.search(str(unidecode.unidecode(p)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                    if re.search(str(p),str(item.nome),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                return l
        except:
            pass
        
        return lojas


class categoria(ListView):
    model = Lojas
    paginate_by = 20
    context_object_name = 'lojas'
    template_name = 'home/testes/categoria.html'
    ordering = ['nome']
    
    def get_queryset(self):
        lojas = ""
        cat = ""
        if self.request.user.is_authenticated:
            try:
                """
                Tenta filtrar quais lojas entregam em sua residencia,
                caso não consiga filtrar retornara todas as lojas cadastras no site
                """  
                u = usuarios.objects.get(id=self.request.user.id)
                end = enderecos.objects.get(cliente=u)
                c = end.CEP
                x = criarLista(c)
                lojas = x
                
            except:
                """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
                ira retornar todas as lojas cadastradas"""
                lojas = Lojas.objects.all()
        else:
            lojas = Lojas.objects.all()

        cat = categoria=self.kwargs['categoria']
        l = []
        for loja in lojas:
            if str(cat) == 'comida':
                if loja.categoria.categoria == 'Restaurantes':
                    l.append(loja)
                
                if loja.categoria.categoria == 'Pizzarias':
                    l.append(loja)

                if loja.categoria.categoria == 'Lanchonetes':
                    l.append(loja)
            else:
                if str(loja.categoria) == str(cat):
                    l.append(loja)
        lojas = l
        try:
            if self.request.GET['pesquisa']:
                import re
                import unidecode
                p = self.request.GET['pesquisa']
                l = []
                lista = lojas
                for item in lista:
                    encontrou = False
                    if re.search(str(p),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                        l.append(item)
                        encontrou = True
                    if re.search(str(unidecode.unidecode(p)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                    if re.search(str(p),str(item.nome),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                return l
        except:
            pass
        
        return lojas

class lista(ListView):
    model = Produtos
    paginate_by = 5
    context_object_name = 'Produtos'
    template_name = 'home/lista.html'
    ordering = ['nome']

"""class testelista(ListView):
    template_name = 'home/teste.html'
    model = Produtos.objects.filter(id_loja=
    paginate_by = 5
    context_object_name = 'produtos'
    ordering = ['nome']
    def get_context_data(self,**kwargs):
        context = super(testelista,self).get_context_data(**kwargs)
        context['produtos'] = Produtos.objects.filter(id_loja=self.kwargs['id'])
        
        
        return context"""

class loja(ListView):
    paginate_by = 20
    model = Produtos
    template_name = 'home/loja.html'

    context_object_name = 'produtos'
    def get_queryset(self):
        import re
        import unidecode
        try:
            if self.request.GET['pesquisa']:
                p = self.request.GET['pesquisa']
                l = []
                lista = self.model.objects.filter(id_loja=self.kwargs['id'])
                for item in lista:
                    encontrou = False
                    if re.search(str(p),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                        l.append(item)
                        encontrou = True
                    if re.search(str(unidecode.unidecode(p)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                    if re.search(str(p),str(item.nome),re.IGNORECASE) and encontrou == False:
                        l.append(item)
                        encontrou = True
                return l
            else:
                return self.model.objects.filter(id_loja=self.kwargs['id'])
        except:
            return self.model.objects.filter(id_loja=self.kwargs['id'])
    def get_context_data(self,**kwargs):
        context = super(loja,self).get_context_data(**kwargs)
        #context['produtos'] = Produtos.objects.filter(id_loja=self.kwargs['id_loja'])
        context['itens'] = []
        obj = []
        request = self.request
        if request.user.is_authenticated:
            obj = ""
            #verifica se o usuario quais prdoutos o usuario tem no carrinho, e se o usuario não é uma loja
            try:
                usu = usuarios.objects.get(pk=request.user.id)
                try:
                    obj = SubPedido.objects.filter(pedidos__pk=usu.ultimopedido)
                    for item in obj:
                        context['itens'].append(item.item)
                       
                except:
                    
                    obj = ""
            except:
                pass
        return context

        
    

