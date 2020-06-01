from django.db import models


class CEP(models.Model):
    CEP  = models.CharField(max_length=10)
    Coordenadas = models.CharField(max_length=60)
    endereco = models.CharField(max_length=100,blank=True, null=True)
    
    objects = models.Manager()

    def __str__(self):
        return self.CEP


class solicitacoes_geo(models.Model):
    data = models.CharField(max_length=12)
    hora = models.CharField(max_length=9)
    ender = models.CharField(max_length=100)
