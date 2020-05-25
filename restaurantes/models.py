from django.db import models
from cadastros.models import Lojas
from produtos.models import Produtos
from django.shortcuts import get_object_or_404

class produto_restaurante(models.Model):
    nome = models.CharField(max_length=50)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE,blank=True,null=True)
    id_loja =models.ForeignKey(Lojas,on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200,verbose_name='Descrição')
    foto = models.ImageField(upload_to='produtos')
    valor = models.DecimalField(max_digits=5,decimal_places=2)
    objects = models.Manager()


    def save(self, *args, **kwargs):
        p = Produtos(id_loja=self.id_loja,
        nome=self.nome,
        valor=self.valor,
        imagem=self.foto)
        p.save()
        self.produto = p

        super().save(*args, **kwargs)


    def __str__(self):
        return self.nome

class bebidas(models.Model):
    nome = models.CharField(max_length=50)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE,blank=True,null=True)
    id_loja =models.ForeignKey(Lojas,on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='produtos', blank=True,null=True)
    valor = models.DecimalField(max_digits=5,decimal_places=2)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        p = Produtos(id_loja=self.id_loja,
        nome=self.nome,
        valor=self.valor,
        imagem=self.foto)
        p.save()
        self.produto = p
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome



"""class Transferencia(models.Model):
    n1 = models.IntegerField()
    n2 = models.IntegerField()
    total = models.IntegerField(null=True,blank=True)

    def save(self, *args, **kwargs):
        x = self.n1 * self.n2
        self.total = x
        super().save(*args, **kwargs)"""