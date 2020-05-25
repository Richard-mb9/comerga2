from django.urls import path
from .views import Painel
from .views import Criar_pagamentos
from .views import extrato




urlpatterns = [
    path('Painel-admin', Painel,name='painel_admin'),
    path('criar-pagamentos',Criar_pagamentos,name='criar_pagamentos'),
    path('extrato',extrato,name='extrato'),
]