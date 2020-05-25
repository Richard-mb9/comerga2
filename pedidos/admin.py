from django.contrib import admin
from .models import pedidos
from .models import SubPedido

admin.site.register(pedidos)
admin.site.register(SubPedido)
