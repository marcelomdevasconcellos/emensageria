"""dag_django_autogenerate URL Configuration

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
from django.contrib import admin
from django.urls import path
from esocial.views import (
    dashboard_json, 
    visualizar_xml, 
    eventos_api_detail, 
    eventos_api_list)

app_name = 'esocial'

urlpatterns = [
    path('dashboard-json/', 
        dashboard_json, name='dashboard_json'),
    path('visualizar-xml/<int:pk>/', 
        visualizar_xml, name='visualizar_xml'),
    path('api/',
        eventos_api_list.as_view() ),
    path('api/<int:pk>/',
        eventos_api_detail.as_view() ),
]
