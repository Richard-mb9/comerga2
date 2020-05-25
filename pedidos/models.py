from django.db import models
from cadastros.models import usuarios
from produtos.models import Produtos
from cadastros.models import Lojas

class SubPedido(models.Model):
    Quantidade = models.DecimalField(max_digits=4,decimal_places=1)
    item = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    loja = models.ForeignKey(Lojas, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return(str(self.pk))
    


class pedidos(models.Model):
    pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=150,verbose_name='Observação',null=True,blank=True)
    itens = models.ManyToManyField(SubPedido, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data = models.DateField(blank=True,null=True)
    pedidofechado = models.CharField(default="não", max_length=5, null=True) 
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    taxa_servico = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    forma_de_pagamento = models.CharField(max_length=10,null=True,blank=True)
    troco = models.CharField(max_length=10,null=True,blank=True)
    valor_troco = models.CharField(max_length=10,null=True,blank=True)
    status_entrega = models.CharField(default="não entregue",max_length=15)
    status_pagamento = models.CharField(default="não pago",max_length=10)
    pedido_cancelado = models.CharField(default="não",max_length=5)
    motivo_cancelamento = models.TextField(default="", max_length=300)
    CEP = models.CharField(max_length=11, blank=True, null=True)
    Rua = models.CharField(max_length=50,blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    complemento = models.CharField(max_length=25,blank=True, null=True)
    Cidade = models.CharField(max_length=50,blank=True, null=True)
    Estado = models.CharField(max_length=30, blank=True, null=True)
    objects = models.Manager()
    
    def __str__(self):
        return (str(self.pedido))