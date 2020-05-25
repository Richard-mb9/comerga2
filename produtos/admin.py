from django.contrib import admin
from .models import Produtos
from .models import imagens_produtos

admin.site.register(Produtos)
admin.site.register(imagens_produtos)
