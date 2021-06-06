from rest_framework.routers import DefaultRouter
from .viewsets import (
    EventosViewSet, )

router = DefaultRouter()
router.register(r'eventos', EventosViewSet, basename='eventos')
urlpatterns = router.urls