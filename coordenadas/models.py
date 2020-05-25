from django.db import models


class CEP(models.Model):
    CEP  = models.CharField(max_length=10)
    Coordenadas = models.CharField(max_length=60)
    endereco = models.CharField(max_length=100,blank=True, null=True)
    
    objects = models.Manager()

    def __str__(self):
        return self.CEP

