from django.contrib import admin
from .models import usuarios
from .models import Lojas
from .models import enderecos
from .models import arquivos
from .models import categorias_lojas
from .models import horarios

admin.site.register(usuarios)
admin.site.register(Lojas)
admin.site.register(enderecos)
admin.site.register(arquivos)
admin.site.register(categorias_lojas)