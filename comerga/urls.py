from django.contrib import admin
from django.urls import path, include
from cadastros import urls as urls_cadastros
from pedidos import urls as urls_pedidos
from home import urls as urls_home
from produtos import urls as urls_produtos
from pagamentos import urls as urls_pagamentos
from Transferencias import urls as urls_transferencias
from restaurantes import urls as urls_restaurantes
from django.conf import settings
from django.conf.urls.static import static
from cadastros.views import logout_view
from pedidos.views import calculo_pedido
from cadastros.views import logar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(urls_home) ),
    path('',include(urls_cadastros)),
    path('',include(urls_produtos)),
    path('',include(urls_pedidos)),
    path('',include(urls_pagamentos)),
    path('',include(urls_transferencias)),
    path('',include(urls_restaurantes)),
    #path('accounts/', include('django.contrib.auth.urls'),name='login'),
    path('accounts/login/', logar,name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
