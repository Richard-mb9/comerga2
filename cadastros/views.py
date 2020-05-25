from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .forms import form_usuarios
from .forms import form_endereco
from .forms import form_loja
from .forms import form_arquivos
from .models import usuarios
from .models import enderecos
from .models import horarios
from django.contrib.auth.models import User
from produtos.models import Produtos
from pedidos.models import pedidos
import pandas as pd
from cadastros.models import arquivos
from cadastros.models import Lojas
from produtos.forms import form_produto
import json
from json import loads
import os
from django.core.mail import send_mail
import smtplib
from django.core import mail
from coordenadas.coordenadas import criarEndereco,coordenadas
from coordenadas.models import  CEP
from datetime import datetime

""" Quando o usuario esta se cadastrando, esta função verifica
se ja aquele email ja foi cadastrado por outro usuario"""
@csrf_exempt
def verifica_email(req):
    resposta = ""
    obj = loads(req.body)
    email = obj['email']
    username = ""
    try:
        username = User.objects.get(username=email)
    except:
        pass
    
    if username:
        print(username)
        resposta = {'resposta':False}
    else:
        resposta = {'resposta':True}
        print("usuario não encontrado")

    return HttpResponse(json.dumps(resposta))



def salvar_cooredenadas(CEP):
    try:
        ender = criarEndereco(CEP)
        coord = coordenadas(ender)
        salvar_cep = CEP(CEP=CEP,Coordenadas=coord,endereco=ender)
        salvar_cep.save()
    except:
        pass

def logar(req):
    if req.method == 'POST':
        name = req.POST['username'].lower()
        senha = req.POST['password']
        user = authenticate(username=name, password=senha)
        if user is not None:
            if user.is_active:
                login(req, user)
                return redirect('home')
            else:
                return HttpResponse("erro")
        else:
            return render(req,'registration/login.html',
            {'mensagem':"Nome de usuario ou senha Invalidos, verifique letras maiusculas e minusculas"})
    return render(req, 'registration/login.html')
    

def buscarUsuario(email,senha,confirm):
    usu = User.objects.all()
    alerta = ""
    for usu in usu:
        if usu.username == email:
            return ("nome Repetido")
    if senha != confirm:
        return ("senhas diferentes")
    if alerta == "":
        return("")

@login_required
def logout_view(req):
    logout(req)
    return redirect('home')


def novoUsuario(req):   
    form = form_usuarios(req.POST or None, req.FILES or None)
    
    if form.is_valid():
        email = form.cleaned_data["email"]
        nome = form.cleaned_data["Primeiro_nome"]
        senha = form.cleaned_data["senha"]
        confirm = form.cleaned_data["confirm"]
        login = email.lower()

        alerta = buscarUsuario(email,senha,confirm)

        if alerta =="":
            user = User.objects.create_user(login)
            user.username = email.lower()
            user.password = senha
            user.first_name = nome
            user.set_password(user.password)
            user.save()
            l =form.save(commit=False)
            l.email = email.lower()
            l.id = user.id
            l.save()
            return redirect('login')
    return render(req, 'cadastros/novo-usuario.html',{'form':form})

@login_required
def novoEndereco(req):
    form = form_endereco(req.POST or None)
    usu = get_object_or_404(usuarios, pk=req.user.id)
    form.fields['cliente'].initial = usu
    if form.is_valid():
        #f = form.save(commit=False)
        #f.cliente = usu
        CEP = form.cleaned_data['CEP']
        salvar_cooredenadas(CEP)
        form.save()
        #f.save()
        return redirect('home')
    else:
        print(form)
    return render(req,'cadastros/novo-endereco.html',{'form':form, 'usuario':usu})

def novaLoja(req):
    form = form_loja(req.POST or None, req.FILES or None)
    if req.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data["email"]
            nome = form.cleaned_data["nome"]
            senha = form.cleaned_data["senha"]
            login = email
            CEP = form.cleaned_data['CEP']
            salvar_cooredenadas(CEP)
            user = User.objects.create_user(login)
            user.username = email.lower()
            user.password = senha
            user.first_name = nome
            user.set_password(user.password)
            user.save()
            l =form.save(commit=False)
            l.email = email.lower()
            l.id = user.id
            l.save()
            loja = get_object_or_404(Lojas,pk=l.id)
            post = req.POST
            p = horarios(loja=loja,
            seg_abre=post['seg_abre'],seg_fecha=post['seg_fecha'],
            ter_abre=post['ter_abre'],ter_fecha=post['ter_fecha'],
            qua_abre=post['qua_abre'],qua_fecha=post['qua_fecha'],
            qui_abre=post['qui_abre'],qui_fecha=post['qui_fecha'],
            sex_abre=post['sex_abre'],sex_fecha=post['sex_fecha'],
            sab_abre=post['sab_abre'],sab_fecha=post['sab_fecha'],
            dom_abre=post['dom_abre'],dom_fecha=post['dom_fecha']
            )
            p.save()
            return redirect('login')
        else:
            print(form._errors)
            for item in req.POST:
                print (req.POST[item])
    
    return render (req, 'cadastros/nova-loja.html', {'form':form})

    
@login_required
def criar_varios_produtos(req):
    try:
        arq = get_object_or_404(arquivos,cliente=req.user.id)
        os.remove("media/" + str(arq.arquivo)) 
        arq.delete()
    except:
        pass  
    form = form_arquivos(req.POST or None, req.FILES or None)
    form.fields['cliente'].initial=req.user.id
    if form.is_valid():
        form.save()
        return redirect ('cadastrando')
    return render(req,'cadastros/cadastrar_varios.html', {'form':form})


#cadastra varios produtos de uma unica vez por meio de um arquivo excel
@login_required
def cadastrando(req):
    #arq = get_object_or_404(arquivos,cliente=req.user.id)
    a = arquivos.objects.filter(cliente=req.user.id)  
    loj = get_object_or_404(Lojas,pk=req.user.id)
    arq = a[-1]
    i = 0
    x = pd.read_excel(arq.arquivo)
    
    print(x)
    #os.remove("media/" + str(arq.arquivo))
    while i < len(x):
        f = Produtos(
            id_loja = loj,
            codigo_de_barras=int(x.loc[i,'codigo']),
            nome = str(x.loc[i,'descricao']),
            valor = float((x.loc[i,'valor'])),
            produto_pesavel = str(x.loc[i,'Pesavel']),
            imagem = "#"
        )
        f.save()
        i += 1
    
    return redirect('produtos-cadastrados', req.user.id)


#cria uma lista com todos os pedidos do cliente logado
@login_required
def meus_pedidos(req):
    usu = get_object_or_404(usuarios, id=req.user.id)
    ped = pedidos.objects.filter(cliente=usu)
    for p in ped:
        if p.data:
            p.data = p.data.strftime("%d/%m/%Y")
        else:
            p.data = datetime.today()
            p.data = p.data.strftime("%d/%m/%Y")
    ped = reversed(ped)
    
    return render(req, 'cadastros/meus_pedidos.html', {'pedidos':ped})


def busca_loja(username):
        loja = Lojas.objects.filter(email=username)
        if len(loja) != 0:
            return True
        else:
            return False


#cria uma lista com todos os dados do cliente
@login_required
def meus_dados(req):
    ender = ""
    e_loja = busca_loja(req.user.username)
    if e_loja ==True:
        usu = get_object_or_404(Lojas, pk=req.user.id)
        return render(req, 'cadastros/meus_dados_loja.html', {'loja':usu})
    else:
        usu = get_object_or_404(usuarios, pk=req.user.id)
        ender = get_object_or_404(enderecos,cliente=usu)
        return render(req, 'cadastros/meus_dados.html', {'endereco':ender, 'usuario':usu})
    
    

    return render(req, 'cadastros/meus_dados.html', {'endereco':ender, 'usuario':usu})


#altera os dados do cliente e das lojas
@login_required
def alterar_cadastro_usuario(req):
    e_loja = busca_loja(req.user.username)
    if e_loja==True:
        usu = get_object_or_404(Lojas,pk=req.user.id)
        form = form_loja(req.POST or None, instance=usu)
        if req.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('meus_dados')
        return render(req, 'cadastros/alterar_dados_loja.html',{'form':form, 'usu':usu})
    else:
        usu = get_object_or_404(usuarios, pk=req.user.id)
        form = form_usuarios(req.POST or None, instance=usu)
        if req.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('meus_dados')
        return render(req, 'cadastros/alterar_dados_cliente.html',{'form':form, 'usu':usu})
    
    return render(req, 'cadastros/alterar_dados_cliente.html',{'form':form, 'usu':usu})


#pagina para alterar o endereço do cliente(apenas para clientes)
def alterar_endereço(req):
    usu = get_object_or_404(usuarios, pk=req.user.id)
    ender = get_object_or_404(enderecos,cliente=usu)
    form = form_endereco(req.POST or None, instance=ender)

    if req.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('meus_dados')

    return render(req, 'cadastros/alterar_endereco.html', {'form':form, 'usuario':usu})

#envia a senha para o email do usuario(apenas se ele for cadastrado)
def esqueceuSenha(req):
    de = "comerga.comercio@gmail.com"
    email = ""
    senha = ""
    msg = ""
    if req.method =="POST":
        email = req.POST['email']
        a = encontrarEmail(email)
        if a == "lojas":
            u = get_object_or_404(Lojas, email=email)
            senha = u.senha
            msg = "A sua senha e - ".encode('utf-8') + str(senha).encode('utf-8')
        elif a == "usuarios":
            u = get_object_or_404(usuarios, email=email)
            senha = u.senha
            msg = "A sua senha e - ".encode('utf-8') + str(senha).encode('utf-8')
        elif a == "vazio":
            msg = str("email não Encontrado no nosso sistema").encode('utf-8')
        
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(de,'Ww12Ric8')
        server.sendmail(de,
        email,
        msg
        )
        server.quit()
        

    return render(req, 'cadastros/esqueceu_senha.html')



def encontrarEmail(email):
    usu = usuarios.objects.filter(email=email)
    if len(usu) == 0:
        u = Lojas.objects.filter(email=email)
        if len(u) != 0:
            return "lojas"
        else:
            return "vazio"
        
    else:
        return "usuarios"








    

