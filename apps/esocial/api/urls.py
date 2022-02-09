from rest_framework.routers import DefaultRouter
from .viewsets import (
    EventosViewSet, TransmissorViewSet, )

router = DefaultRouter()
router.register(r'eventos', EventosViewSet, basename='eventos')
router.register(r'transmissores', TransmissorViewSet, basename='transmissores')
urlpatterns = router.urls