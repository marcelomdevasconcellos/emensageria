""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.urls import path, include

from .views import *

app_name = 'esocial'

urlpatterns = [

    path('dashboard-json/',
         dashboard_json,
         name='dashboard_json'),

    path('validar-evento/<int:pk>/',
         validar_evento,
         name='validar_evento'),

    path('validar-eventos/',
         validar_eventos,
         name='validar_eventos'),

    path('visualizar-xml/<int:pk>/',
         visualizar_xml,
         name='visualizar_xml'),

    path("api/", include("apps.esocial.api.urls")),

    path('consultar-evento/<int:pk>/',
         consultar_evento,
         name='consultar_evento'),

    path('consultar-transmissor/<int:pk>/',
         consultar_transmissor,
         name='consultar_transmissor'),

    path('consultar-transmissor/',
         consultar_transmissores,
         name='consultar_transmissores'),

    path('enviar-evento/<int:pk>/',
         enviar_evento,
         name='enviar_evento'),

    path('enviar-transmissor/<int:pk>/',
         enviar_transmissor,
         name='enviar_transmissor'),

    path('enviar-transmissores/',
         enviar_transmissores,
         name='enviar_transmissores'),

    path('evento/recibo/<int:pk>/',
         eventos_recibo,
         name='eventos_recibo'),

    path('transmissor/recibo/<int:pk>/',
         transmissores_recibo,
         name='transmissores_recibo'),

    path('relatorios/imprimir/<int:pk>/',
         relatorios_imprimir,
         name='relatorios_imprimir'),

    path('arquivos/visualizar/<int:pk>/',
         arquivos_visualizar,
         name='arquivos_visualizar'),

    # path('arquivos/reprocessar/<int:pk>/',
    #     arquivos_reprocessar, 
    #     name='arquivos_reprocessar'),

    # path('arquivos/recuperar/<int:pk>/',
    #     arquivos_recuperar, 
    #     name='arquivos_recuperar'),

]
