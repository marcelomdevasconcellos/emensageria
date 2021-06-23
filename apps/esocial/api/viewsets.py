from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import redirect, get_object_or_404, render

from django.forms.models import model_to_dict
from .serializers import EventosSerializer
from ..models import Eventos
from ..choices import EVENTO_ORIGEM_API


class EventosViewSet(ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer
    search_fields = ['identidade', ]
    http_method_names = ['get', 'put', 'patch', 'post', 'head']
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='atualizar-identidade')
    def atualizar_identidade(self, request, pk=None):
        obj = get_object_or_404(Eventos, id=pk)
        obj.make_identidade()
        return Response(model_to_dict(obj))

    @action(detail=True, methods=['get'], url_path='abrir')
    def abrir_evento_para_edicao(self, request, pk=None):
        obj = get_object_or_404(Eventos, id=pk)
        obj.abrir_evento_para_edicao()
        return Response(model_to_dict(obj))

    @action(detail=True, methods=['get'], url_path='validar')
    def validar(self, request, pk=None):
        obj = get_object_or_404(Eventos, id=pk)
        obj.validar()
        return Response(model_to_dict(obj))

    @action(detail=True, methods=['get'], url_path='enviar')
    def enviar(self, request, pk=None):
        obj = get_object_or_404(Eventos, id=pk)
        obj.enviar()
        return Response(model_to_dict(obj))

    @action(detail=True, methods=['get'], url_path='consultar')
    def consultar(self, request, pk=None):
        obj = get_object_or_404(Eventos, id=pk)
        obj.consultar()
        return Response(model_to_dict(obj))
