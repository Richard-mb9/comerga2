from django.db import models
from django.contrib import admin
from cadastros.models import Lojas
from datetime import datetime,timedelta
from django.shortcuts import get_object_or_404

"""class Transferencia(models.Model):
    n1 = models.IntegerField()
    n2 = models.IntegerField()
    total = models.IntegerField(null=True,blank=True)

    def save(self, *args, **kwargs):
        x = self.n1 * self.n2
        self.total = x
        super().save(*args, **kwargs)"""


class Transferencias(models.Model):
    data = models.DateField()
    loja = models.ForeignKey(Lojas,on_delete=models.CASCADE)
    Banco = models.CharField(max_length=25, null=True,blank=True)
    agencia = models.CharField(max_length=8,null=True,blank=True)
    digito_agencia = models.CharField(max_length=2 ,verbose_name='digito da agência', null=True,blank=True)
    conta = models.CharField(max_length=8,null=True,blank=True)
    digito_conta = models.CharField(max_length=2,verbose_name="digito da conta", null=True,blank=True)
    valor = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    status = models.CharField(max_length=10,default='agendado')
    objects = models.Manager()