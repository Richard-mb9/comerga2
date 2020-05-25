from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cadastros.models import Lojas
from cadastros.models import enderecos
from produtos.models import Produtos
from pedidos.views import TotalCarrinho
from pedidos.views import calcular_saldo_loja
from pedidos.models import SubPedido
from cadastros.models import usuarios
from cadastros.models import horarios
from django.http import HttpResponse
from json import loads
import json
from coordenadas.coordenadas import criarLista
import unidecode
import re
from datetime import datetime,timedelta,date,time

n= 20

#n é quantidade de itens que deseja que tenha em cada sublista
def dividir_lista(lista,n):
    x = lista
    v = []
    sublista = []
    for xn in x:
        if len(sublista) < n:
            sublista.append(xn)
        else:
            v.append(sublista)
            sublista = []
            sublista.append(xn)
    v.append(sublista)
    return v


def verificar_horario(loja):
    l = get_object_or_404(Lojas,pk=loja.id)
    h = "x"
    try:
        h = get_object_or_404(horarios,loja=l)
    except:
        pass

    DIAS = [
    'seg',
    'ter',
    'qua',
    'qui',
    'sex',
    'sab',
    'dom'
    ]

    data = datetime.today()
    hour = str(datetime.now().hour) + "." + str(datetime.now().minute)
    hour = float(hour)
    indice_da_semana = data.weekday()
    dia_da_semana = DIAS[indice_da_semana]

    if h != 'x':
        if dia_da_semana == 'seg':
            if hour >= h.seg_abre and hour <= h.seg_fecha:
                return True
            else:
                return False
        if dia_da_semana == 'ter':
            if hour >= h.ter_abre and hour <= h.ter_fecha:
                return True
            else:
                return False
        if dia_da_semana == 'qua':
            if hour >= h.qua_abre and hour <= h.qua_fecha:
                return True
            else:
                return False
        if dia_da_semana == 'qui':
            if hour >= h.qui_abre and hour <= h.qui_fecha:
                return True
            else:
                return False               
        if dia_da_semana == 'sex':
            if hour >= h.sex_abre and hour <= h.sex_fecha:
                return True
            else:
                return False
        if dia_da_semana == 'sab':
            if hour >= h.sab_abre and hour <= h.sab_fecha:
                return True
            else:
                return False
        if dia_da_semana == 'dom':
            if hour >= h.dom_abre and hour <= h.dom_fecha:
                return True
            else:
                return False
                
    else:
        return True


#inicio da aplicação
def index(req):
    is_loja = False
    if req.user.is_authenticated:
        u = Lojas.objects.filter(pk=req.user.id)
        if len(u) == 1:
            is_loja = True
        else:
            is_loja = False
    if is_loja == True:
        return redirect('vender')
    else:
        return redirect('index',page=0)

def home(req,page):
    #primeiro faz a verifição se o usuario é uma loja
    is_loja = False
    if req.user.is_authenticated:
        try:
            grupo = req.user.groups.all()
            if grupo[0].name == "Administração":
                print('é do grupo')
        except:
            pass
        u = Lojas.objects.filter(pk=req.user.id)
        if len(u) == 1:
            is_loja = True
        else:
            is_loja = False
    if is_loja == True:
        return redirect('vender')


    ender = ""
    lista_lojas = ""

    if req.method == 'POST':
        page = 0
        pesquisa = req.POST['pesquisa']
        if not pesquisa:
            pesquisa = "null"
        return redirect('pesquisa_home',pesquisa,page)
    
    if req.user.is_authenticated:
        try:
            usu = usuarios.objects.filter(id=req.user.id)
        except:
            lista_lojas = Lojas.objects.all()
        if len(usu) != 0:
            try:
                ender = enderecos.objects.filter(cliente=req.user.id)
                qt = len(ender)
                if qt == 0:
                    try:
                        return redirect ('novo-endereco')
                    except:
                        pass
            except:
                pass
        try:
            """
            Tenta filtrar quais lojas entregam em sua residencia,
            caso não consiga filtrar retornara todas as lojas cadastras no site
            """  
            u = get_object_or_404(usuarios, pk=req.user.id)
            end = get_object_or_404(enderecos, cliente=u)
            c = end.CEP
            x = criarLista(c)
            lista_lojas = x
            
        except:
            """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
            ira retornar todas as lojas cadastradas"""
            lista_lojas = Lojas.objects.all()
        
    else:
        lista_lojas = Lojas.objects.all()
    

    a = []
    #for loja in lista_lojas:
        #if verificar_horario(loja) == True:
           # a.append(loja)
    
    #lista_lojas = a
    sublistas = dividir_lista(lista_lojas,n)
    lista_lojas = sublistas[page]
    voltar = page - 1
    #print(obj[0])
    if page < len(sublistas) -1:
        page += 1
    else:
        page = 'ultima'
    
    print("IP: " + str(req.META['REMOTE_ADDR']))
    
    return render(req,'home/home.html', {'lojas':lista_lojas,'carregar_mais':page,
    'voltar':voltar})

def home_categoria(req,categoria,page):
    ender = ""
    lista_lojas = ""

    if req.method == 'POST':
        page = 0
        pesquisa = req.POST['pesquisa']
        if not pesquisa:
            pesquisa = "null"
        return redirect('pesquisa_categoria',categoria,pesquisa,page)
    
    if req.user.is_authenticated:
        try:
            usu = usuarios.objects.filter(id=req.user.id)
        except:
            lista_lojas = Lojas.objects.all()
        if len(usu) != 0:
            try:
                ender = enderecos.objects.filter(cliente=req.user.id)
                qt = len(ender)
                if qt == 0:
                    try:
                        return redirect ('novo-endereco')
                    except:
                        pass
            except:
                pass
        try:
            """
            Tenta filtrar quais lojas entregam em sua residencia,
            caso não consiga filtrar retornara todas as lojas cadastras no site
            """  
            u = get_object_or_404(usuarios, pk=req.user.id)
            end = get_object_or_404(enderecos, cliente=u)
            c = end.CEP
            x = criarLista(c)
            lista_lojas = x
            
        except:
            """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
            ira retornar todas as lojas cadastradas"""
            lista_lojas = Lojas.objects.all()
        
    else:
        lista_lojas = Lojas.objects.all()
    
    
    l = []
    for loja in lista_lojas:
        if str(categoria) == 'comida':
            if loja.categoria.categoria == 'Restaurantes':
                l.append(loja)
            
            if loja.categoria.categoria == 'Pizzarias':
                l.append(loja)

            if loja.categoria.categoria == 'Lanchonetes':
                l.append(loja)
        else:
            if str(loja.categoria) == str(categoria):
                l.append(loja)
    
    lista_lojas = l
    sublistas = dividir_lista(lista_lojas,n)
    lista_lojas = sublistas[page]
    voltar = page - 1
    #print(obj[0])
    if page < len(sublistas) -1:
        page += 1
    else:
        page = 'ultima'
    
    print("IP: " + str(req.META['REMOTE_ADDR']))
    
    return render(req,'home/home_categoria.html', {'lojas':lista_lojas,'carregar_mais':page,
    'voltar':voltar})


def pesquisa_categorias(req,categoria,pesquisa,page):
    ender = ""
    lista_lojas = ""
    if req.user.is_authenticated:
        try:
            usu = usuarios.objects.filter(id=req.user.id)
        except:
            lista_lojas = Lojas.objects.all()
        if len(usu) != 0:
            try:
                ender = enderecos.objects.filter(cliente=req.user.id)
                qt = len(ender)
                if qt == 0:
                    try:
                        return redirect ('novo-endereco')
                    except:
                        pass
            except:
                pass
        try:
            """
            Tenta filtrar quais lojas entregam em sua residencia,
            caso não consiga filtrar retornara todas as lojas cadastras no site
            """  
            u = get_object_or_404(usuarios, pk=req.user.id)
            end = get_object_or_404(enderecos, cliente=u)
            c = end.CEP
            x = criarLista(c)
            lista_lojas = x
            
            
        except:
            """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
            ira retornar todas as lojas cadastradas"""
            lista_lojas = Lojas.objects.all()
        
    else:
        lista_lojas = Lojas.objects.all()

    if req.method == 'POST':
            import re
            import unidecode
            pesquisa = req.POST['pesquisa']
            l = []
            for item in lista_lojas:
                encontrou = False
                if re.search(str(pesquisa),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
                if re.search(str(unidecode.unidecode(pesquisa)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
                if re.search(str(pesquisa),str(item.nome),re.IGNORECASE) and encontrou == False:
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
            lista_lojas = l
            page = 0
    

    else:
        #aqui fara o filtro da pesquisa que foi feita
        if pesquisa != "null":
            l = []
            for item in lista_lojas:
                import re
                import unidecode
                encontrou = False
                if re.search(str(pesquisa),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
                if re.search(str(unidecode.unidecode(pesquisa)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
                if re.search(str(pesquisa),str(item.nome),re.IGNORECASE) and encontrou == False:
                    if str(categoria) == 'comida':
                        if item.categoria.categoria == 'Restaurantes':
                            l.append(item)
                            encontrou = True
                        
                        if item.categoria.categoria == 'Pizzarias':
                            l.append(item)
                            encontrou = True

                        if item.categoria.categoria == 'Lanchonetes':
                            l.append(item)
                            encontrou = True
                    else:
                        if str(item.categoria) == str(categoria):
                            l.append(item)
                            encontrou = True
                lista_lojas = l



    #caso esteja sendo feita uma nova pesquisa sera executada esta função
    
    sublistas = dividir_lista(lista_lojas,n)
    lista_lojas = sublistas[page]
    voltar = page - 1
    if page < len(sublistas) -1:
        page += 1
    else:
        page = 'ultima'
    
    return render(req,'home/home_categoria.html', {'lojas':lista_lojas,'carregar_mais':page,
    'voltar':voltar})


#pagina de pesquisa ta tela inicial
def pesquisa_home(req,pesquisa,page):
    ender = ""
    lista_lojas = ""
    if req.user.is_authenticated:
        try:
            usu = usuarios.objects.filter(id=req.user.id)
        except:
            lista_lojas = Lojas.objects.all()
        if len(usu) != 0:
            try:
                ender = enderecos.objects.filter(cliente=req.user.id)
                qt = len(ender)
                if qt == 0:
                    try:
                        return redirect ('novo-endereco')
                    except:
                        pass
            except:
                pass
        try:
            """
            Tenta filtrar quais lojas entregam em sua residencia,
            caso não consiga filtrar retornara todas as lojas cadastras no site
            """  
            u = get_object_or_404(usuarios, pk=req.user.id)
            end = get_object_or_404(enderecos, cliente=u)
            c = end.CEP
            x = criarLista(c)
            lista_lojas = x
            
            
        except:
            """caso não consiga filtrar as lojas que fassam entrega na sua residencia, 
            ira retornar todas as lojas cadastradas"""
            lista_lojas = Lojas.objects.all()
        
    else:
        lista_lojas = Lojas.objects.all()

    if req.method == 'POST':
            import re
            import unidecode
            pesquisa = req.POST['pesquisa']
            l = []
            for item in lista_lojas:
                encontrou = False
                if re.search(str(pesquisa),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                    l.append(item)
                    encontrou = True
                if re.search(str(unidecode.unidecode(pesquisa)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                    l.append(item)
                    encontrou = True
                if re.search(str(pesquisa),str(item.nome),re.IGNORECASE) and encontrou == False:
                    l.append(item)
                    encontrou = True
            lista_lojas = l
            page = 0
    
    else:
        #aqui fara o filtro da pesquisa que foi feita
        if pesquisa != "null":
            l = []
            for item in lista_lojas:
                import re
                import unidecode
                encontrou = False
                if re.search(str(pesquisa),str(unidecode.unidecode(item.nome)),re.IGNORECASE):
                    l.append(item)
                    encontrou = True
                if re.search(str(unidecode.unidecode(pesquisa)),str(unidecode.unidecode(item.nome)),re.IGNORECASE) and encontrou == False:
                    l.append(item)
                    encontrou = True
                if re.search(str(pesquisa),str(item.nome),re.IGNORECASE) and encontrou == False:
                    l.append(item)
                    encontrou = True
                lista_lojas = l



    #caso esteja sendo feita uma nova pesquisa sera executada esta função
    
    sublistas = dividir_lista(lista_lojas,n)
    lista_lojas = sublistas[page]
    voltar = page - 1
    #print(obj[0])
    if page < len(sublistas) -1:
        page += 1
    else:
        page = 'ultima'
    
    print("IP: " + str(req.META['REMOTE_ADDR']))
    
    return render(req,'home/pesquisa_home.html', {'lojas':lista_lojas,'carregar_mais':page,
    'voltar':voltar})


#cria uma lista com todos os produtos da loja selecionada pelo cliete
def loja(req,id,pesquisa,page):
    from produtos.models import imagens_produtos
    usu = ""
    lista = Produtos.objects.filter(id_loja=id)
    loja = get_object_or_404(Lojas,pk=id)

    if loja.categoria.categoria == 'Restaurantes':
        return redirect('restaurante',id)
    
    if loja.categoria.categoria == 'Pizzarias':
        return redirect('restaurante',id)

    if loja.categoria.categoria == 'Lanchonetes':
        return redirect('restaurante',id)

    #caso esteja sendo feita uma pesquisa, caso pesquisa seja == p, não esta sendo feita uma pesquisa
    if pesquisa != 'p':
        import re
        import unidecode
        
        p = pesquisa
        
        l = []
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
        lista = l
    
    imagens = []
    produtos_com_imagens =[]
    for item in lista:
        img = ""
        try:
            img = imagens_produtos.objects.get(codigo_de_barras = item.codigo_de_barras)
            imagens.append(img)
            produtos_com_imagens.append(item)
            
        except:
            pass
    itens = ""
    obj = []
    if req.user.is_authenticated:
        #verifica se o usuario quais prdoutos o usuario tem no carrinho, e se o usuario não é uma loja
        try:
            usu = get_object_or_404(usuarios, pk=req.user.id)
            try:
                itens = SubPedido.objects.filter(pedidos__pk=usu.ultimopedido)
                for item in itens:
                    obj.append(item.item)
            except:
                itens = ""
        except:
            pass
        
    #caso esteja sendo feita de algum produto dentro da loja
    if req.method == 'POST':
        import re
        import unidecode
        p = req.POST['pesquisa']
        pesquisa = p
        l = []
        if pesquisa:
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
            lista = l
        else:
            pesquisa = 'p'
        page = 0
        return redirect('loja',id,pesquisa,page)
        


    sublistas = dividir_lista(lista,n)
    lista = sublistas[page]
    voltar = page - 1
    #print(obj[0])
    if page < len(sublistas) -1:
        page += 1
    else:
        page = 'ultima'
    return render(req,'home/loja.html',
    {'lista':lista, 'itens':obj, 'imagens':imagens,
    'pesquisa':pesquisa,'carregar_mais':page, 'loja':id,'voltar':voltar,
    'produtos_com_imagem':produtos_com_imagens})



@csrf_exempt
def verifica_loja(req):
    resposta = ""
    tot_carrinho = 0
    saldo = str(calcular_saldo_loja(req.user.id))
    if req.user.is_authenticated:
        loja = Lojas.objects.filter(email=req.user.username)
        if len(loja) ==0:
            tot_carrinho = str(TotalCarrinho(req.user.id))
            resposta = {'resposta':False,
            'carrinho':tot_carrinho}          
        elif len(loja) == 1:
            resposta = {'resposta':True,
            'carrinho':tot_carrinho,
            'saldo':saldo}
    return HttpResponse(json.dumps(resposta))


#busca todos os subpedidos do cliente para exibilos em uma lista(como se fosse um carrinho de compras)
def busca_sub_pedidos(id):
    usu = get_object_or_404(usuarios, pk=id)
    itens = SubPedido.objects.filter(pedidos__pk=usu.ultimopedido)
    return(itens)

