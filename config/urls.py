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

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

admin.site.site_header = 'eMensageria'
admin.site.site_title = 'eMensageria'
admin.site.index_title = 'eMensageria'


urlpatterns = [
    path('contrib/',
        include("contrib.urls", namespace='contrib')
        ),
    path('esocial/',
        include("esocial.urls", namespace='esocial')
        ),
    path('reinf/',
        include("reinf.urls", namespace='reinf')
        ),
#    path('static/', static),
    path('', admin.site.urls),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
