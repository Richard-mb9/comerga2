from django.db import models
from cadastros.models import Lojas

class Produtos(models.Model):
    id_loja = models.ForeignKey(Lojas, on_delete=models.CASCADE)
    codigo_de_barras = models.DecimalField(default=0, max_digits=13,decimal_places=0)
    nome = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=7,decimal_places=2)
    produto_pesavel = models.CharField(default='não',max_length=5,verbose_name='Produto vendido por peso?')
    imagem = models.ImageField(default='#',blank=True,null=True,upload_to="produtos")
    objects = models.Manager()

    def __str__(self):
        return self.nome
 
class imagens_produtos(models.Model):
    codigo_de_barras = models.IntegerField()
    nome = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to="produtos")
    objects = models.Manager()

    def __str__(self):
        return self.nome
