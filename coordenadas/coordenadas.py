from geopy import distance
import requests
from django.shortcuts import get_object_or_404
import json
from cadastros.models import Lojas,usuarios
from .models import CEP
import credenciais
from datetime import datetime
from .models import solicitacoes_geo


def coordenadas(endereco):
    key = credenciais.KEY_API_GOOGLE
    try:
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + str(endereco) + "&key=" + key)
        results = r.json()['results']
        location = results [0] ['geometry'] ['location']
        d = str(datetime.today().date())
        h = str(datetime.now().hour)
        m = str(datetime.now().minute)
        s = str(datetime.now().second)
        hms = str(h + ":" + m + ":" + s)
        solicitacao = solicitacoes_geo(data=d,hora=hms, ender=endereco)
        solicitacao.save()
        return str(location ['lat']) + "," + str(location ['lng']) 
    except:
        print("erro" + str(Exception))


def distancia(end1, end2):
    dis = distance.distance(end1,end2).kilometers
    return dis

def criarEndereco(cep):
    c = str(cep)
    e = requests.get(f'https://viacep.com.br/ws/{c}/json')
    a = e.json()
    rua = a['logradouro']
    bairro = a['bairro']
    cidade = a['localidade']
    estado = a['uf']
    pais = 'Brasil'
    endereco = str(f"{rua},{bairro},{cidade},{estado},{pais}")
    return(endereco)



def criarLista(cep):
    l = Lojas.objects.all()
    lista = []
    for loj in l:
        print(f"{loj.nome} - CEP {loj.CEP}")
        cep_loj = CEP.objects.filter(CEP=loj.CEP)
        cep_cli = CEP.objects.filter(CEP=cep)
        coord_loj = ""
        coord_cli = ""
        if len(cep_loj) == 1:
            cep_loj = get_object_or_404(CEP,CEP=loj.CEP)
            coord_loj = str(cep_loj.Coordenadas)
        else:
            try:
                end_loja = criarEndereco(loj.CEP)
                coord_loj = coordenadas(end_loja)
                salvar_cep = CEP(CEP=loj.CEP,Coordenadas=coord_loj,endereco=end_loja)
                salvar_cep.save()
            except:
                pass
        if len(cep_cli) == 1:
            cep_cli = get_object_or_404(CEP, CEP=cep)
            coord_cli = str(cep_cli.Coordenadas)
        else:
            try:
                end_cli = criarEndereco(cep)
                coord_cli = coordenadas(end_cli)
                salvar_cep = CEP(CEP=cep,Coordenadas=coord_cli,endereco=end_cli)
                salvar_cep.save()
            except:
                pass

        dis = distancia(coord_cli,coord_loj)
        print(dis)
        if dis <= loj.distancia:
            lista.append(loj)

    print("A lista é " + str(lista))
    return lista

#end1 = coordenadas("26475-390")
#end2 = coordenadas("22250-040")

#print("A distancia é: " + str(distance.distance(end1,end2).kilometers)  + "kms")