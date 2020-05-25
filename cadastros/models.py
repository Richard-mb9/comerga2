from django.db import models
import os

class categorias_lojas(models.Model):
    categoria = models.CharField(max_length=50)
    taxa_servico = models.DecimalField(max_digits=4,decimal_places=2)
    def __str__(self):
        return self.categoria

class usuarios(models.Model):
    id = models.IntegerField(primary_key=True)
    Primeiro_nome = models.CharField(max_length=50,verbose_name='Primeiro Nome')
    Ultimo_nome = models.CharField(max_length=50,verbose_name='Ultimo Nome')
    email = models.EmailField()
    senha = models.CharField(max_length=12)
    confirm = models.CharField(max_length=12,verbose_name='Confirmação de Senha')
    DDD_tel = models.CharField(max_length=3)
    telefone = models.CharField(max_length=9, null=True,blank=True)
    DDD_cel = models.CharField(max_length=3)
    celular = models.CharField(max_length=10)
    ultimopedido = models.CharField(default="#", max_length=15, blank=True,null=True)
    objects = models.Manager()

    def __str__(self):
        return self.Primeiro_nome

class enderecos(models.Model):
    cliente = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    CEP = models.CharField(max_length=9)
    Estado = models.CharField(max_length=50)
    Cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    Rua = models.CharField(max_length=50)
    numero = models.DecimalField(max_digits=5,decimal_places=0)
    complemento = models.CharField(max_length=50,null=True,blank=True)
    latitude = models.CharField(max_length=20,default="")
    longitude = models.CharField(max_length=20,default="")
    objects = models.Manager()

    def __str__(self):
        return self.cliente


class Lojas(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=30, verbose_name='Razão Social')
    CNPJ = models.CharField(max_length=20)
    email = models.EmailField()
    senha = models.CharField(max_length=15)
    confirm = models.CharField(max_length=15)
    DDD_tel = models.IntegerField()
    Telefone = models.CharField(max_length=10)
    DDD_whats = models.IntegerField(null=True, blank=True)
    whatsapp = models.CharField(max_length=10, null=True, blank=True)
    ativa = models.CharField(max_length=4, default="sim")
    categoria = models.ForeignKey(categorias_lojas,on_delete=models.CASCADE)
    CEP = models.CharField(max_length=9)
    Estado = models.CharField(max_length=30)
    Cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    Rua = models.CharField(max_length=50)
    numero = models.DecimalField(max_digits=5,decimal_places=0)
    complemento = models.CharField(max_length=20, null=True,blank=True)
    distancia = models.DecimalField(max_digits=5,decimal_places=0,default=5, verbose_name="Distancia para entregas")
    valor_minimo_frete = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    valor_minimo_compra = models.DecimalField(max_digits=6,decimal_places=2,default=50)
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    Banco = models.CharField(max_length=30)
    agencia = models.CharField(max_length=10)
    digito_agencia = models.CharField(max_length=5, null=True, blank=True)
    conta = models.CharField(max_length=20)
    digito_conta = models.CharField(max_length=5, null=True, blank=True )
    logomarca = models.ImageField( upload_to="media/logomarcas/", null=False, blank=False)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.nome)

class horarios(models.Model):
    loja = models.ForeignKey(Lojas,on_delete=models.CASCADE)
    seg_abre = models.DecimalField(max_digits=4,decimal_places=2)
    seg_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    ter_abre = models.DecimalField(max_digits=4,decimal_places=2)
    ter_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    qua_abre = models.DecimalField(max_digits=4,decimal_places=2)
    qua_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    qui_abre = models.DecimalField(max_digits=4,decimal_places=2)
    qui_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    sex_abre = models.DecimalField(max_digits=4,decimal_places=2)
    sex_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    sab_abre = models.DecimalField(max_digits=4,decimal_places=2)
    sab_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    dom_abre = models.DecimalField(max_digits=4,decimal_places=2)
    dom_fecha = models.DecimalField(max_digits=4,decimal_places=2)
    objects = models.Manager()
    

class arquivos(models.Model):
    cliente = models.ForeignKey(Lojas,on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to="arquivos_excel", null=False, blank=False)
    objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.arquivo.storage.delete()
        super().delete()


