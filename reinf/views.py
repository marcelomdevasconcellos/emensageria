import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reinf.models import (
    Eventos, 
    EventosSerializer, 
    Transmissor, 
    TransmissorEventos, )
from reinf.choices import (
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_IMPORTADO,
    STATUS_EVENTO_DUPLICADO,
    STATUS_EVENTO_GERADO,
    STATUS_EVENTO_GERADO_ERRO,
    STATUS_EVENTO_ASSINADO,
    STATUS_EVENTO_ASSINADO_ERRO,
    STATUS_EVENTO_VALIDADO,
    STATUS_EVENTO_VALIDADO_ERRO,
    STATUS_EVENTO_AGUARD_PRECEDENCIA,
    STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_ENVIADO,
    STATUS_EVENTO_ENVIADO_ERRO,
    STATUS_EVENTO_PROCESSADO,)
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated


def dashboard_json(request):
    import json
    dashboard_data = {
        'reinf_quant_cadastrados': Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO).count(),
        'reinf_quant_importados': Eventos.objects.filter(status=STATUS_EVENTO_IMPORTADO).count(),
        'reinf_quant_erros_validacao': Eventos.objects.filter(status=STATUS_EVENTO_VALIDADO_ERRO).count(),
        'reinf_quant_validados': Eventos.objects.filter(status__in=(STATUS_EVENTO_VALIDADO, STATUS_EVENTO_AGUARD_ENVIO)).count(),
        'reinf_quant_erros_envio': Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO_ERRO).count(),
        'reinf_quant_enviados': Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO).count(),
        'reinf_quant_processados': Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO).count(),
    }
    return HttpResponse(json.dumps(dashboard_data, indent = 4))


class eventos_api_list(generics.ListCreateAPIView):

    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer

    def perform_create(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_ESOCIAL
        from constance import config
        serializer.save(
            criado_por=self.request.user,
            tpamb=config.ESOCIAL_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_ESOCIAL,
            arquivo_original=0,
            status=0)

    def perform_update(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_ESOCIAL
        from constance import config
        serializer.save(
            modificado_por=self.request.user,
            tpamb=config.ESOCIAL_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_ESOCIAL,
            arquivo_original=0,
            status=0)



class eventos_api_detail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer

    def perform_create(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_ESOCIAL
        from constance import config
        serializer.save(
            criado_por=self.request.user,
            tpamb=config.ESOCIAL_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_ESOCIAL,
            arquivo_original=0,
            status=0)

    def perform_update(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_ESOCIAL
        from constance import config
        serializer.save(
            modificado_por=self.request.user,
            tpamb=config.ESOCIAL_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_ESOCIAL,
            arquivo_original=0,
            status=0)


def visualizar_xml(request, pk):

    evt = get_object_or_404(Eventos, id=pk)
    evt.create_xml()

    response = HttpResponse(
        evt.evento_xml,
        content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="%s.xml"' % evt.identidade

    return response
