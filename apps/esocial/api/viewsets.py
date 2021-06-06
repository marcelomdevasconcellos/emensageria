from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import EventosSerializer
from ..models import Eventos


class EventosViewSet(ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer
    search_fields = ['identidade', ]
    http_method_names = ['get', 'put', 'patch', 'post', 'head']
    permission_classes = [IsAuthenticated]
