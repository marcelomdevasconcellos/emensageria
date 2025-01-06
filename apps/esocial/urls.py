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

from django.urls import include, path

from apps.esocial.views.eventos_recibo import eventos_recibo
from apps.esocial.views.parsing_post import parsing_post
from apps.esocial.views.consultar_transmissores import consultar_transmissores
from apps.esocial.views.enviar_transmissores import enviar_transmissores
from apps.esocial.views.consultar_transmissor import consultar_transmissor
from apps.esocial.views.enviar_transmissor import enviar_transmissor
from apps.esocial.views.consultar_evento import consultar_evento
from apps.esocial.views.validar_eventos import validar_eventos
from apps.esocial.views.validar_evento import validar_evento
from apps.esocial.views.enviar_evento import enviar_evento
from apps.esocial.views.visualizar_xml import visualizar_xml
from apps.esocial.views.dashboard_json import dashboard_json

app_name = 'esocial'

urlpatterns = [

    path(
        'dashboard-json/',
        dashboard_json,
        name='dashboard_json'),

    path(
        'validar-evento/<int:pk>/',
        validar_evento,
        name='validar_evento'),

    path(
        'validar-eventos/',
        validar_eventos,
        name='validar_eventos'),

    path(
        'visualizar-xml/<int:pk>/',
        visualizar_xml,
        name='visualizar_xml'),

    path("api/", include("apps.esocial.api.urls")),

    path(
        'consultar-evento/<int:pk>/',
        consultar_evento,
        name='consultar_evento'),

    path(
        'consultar-transmissor/<int:pk>/',
        consultar_transmissor,
        name='consultar_transmissor'),

    path(
        'consultar-transmissor/',
        consultar_transmissores,
        name='consultar_transmissores'),

    path(
        'enviar-evento/<int:pk>/',
        enviar_evento,
        name='enviar_evento'),

    path(
        'enviar-transmissor/<int:pk>/',
        enviar_transmissor,
        name='enviar_transmissor'),

    path(
        'enviar-transmissores/',
        enviar_transmissores,
        name='enviar_transmissores'),

    path(
        'evento/recibo/<int:pk>/',
        eventos_recibo,
        name='eventos_recibo'),

    path('parsing_post/<int:pk>/',
         parsing_post,
         name='parsing_post'),

]
