import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from esocial.models import (
    Eventos, 
    EventosSerializer, 
    Transmissor, 
    TransmissorEventos, )
from esocial.choices import (
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
from .transmissor import enviar, consultar
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated


def dashboard_json(request):
    import json
    eventos_cadastrados = Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO)
    eventos_importados = Eventos.objects.filter(status=STATUS_EVENTO_IMPORTADO)
    eventos_erros_validacao = Eventos.objects.filter(status=STATUS_EVENTO_VALIDADO_ERRO)
    eventos_validados = Eventos.objects.filter(status__in=(STATUS_EVENTO_VALIDADO, STATUS_EVENTO_AGUARD_ENVIO))
    eventos_erros_envio = Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO_ERRO)
    eventos_enviados = Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO)
    eventos_processados = Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO)
    dashboars_data = {
        'esocial_quant_cadastrados': eventos_cadastrados.count(),
        'esocial_quant_importados': eventos_importados.count(),
        'esocial_quant_erros_validacao': eventos_erros_validacao.count(),
        'esocial_quant_validados': eventos_validados.count(),
        'esocial_quant_erros_envio': eventos_erros_envio.count(),
        'esocial_quant_enviados': eventos_enviados.count(),
        'esocial_quant_processados': eventos_processados.count(),
        'esocial_cadastrados': list(eventos_cadastrados.values('id', 'evento', 'identidade')),
        'esocial_importados': list(eventos_importados.values('id', 'evento', 'identidade')),
        'esocial_erros_validacao': list(eventos_erros_validacao.values('id', 'evento', 'identidade')),
        'esocial_validados': list(eventos_validados.values('id', 'evento', 'identidade')),
        'esocial_erros_envio': list(eventos_erros_envio.values('id', 'evento', 'identidade')),
        'esocial_enviados': list(eventos_enviados.values('id', 'evento', 'identidade')),
        'esocial_processados': list(eventos_processados.values('id', 'evento', 'identidade')),
    }
    return HttpResponse(json.dumps(dashboars_data, indent = 4))


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


def enviar_transmissor(request, pk):
    te = get_object_or_404(TransmissorEventos, id=pk)
    dados = enviar(te)
    return HttpResponse('{}', content_type='application/json')


def consultar_transmissor(request, pk):
    te = get_object_or_404(TransmissorEventos, id=pk)
    dados = consultar(te)
    return HttpResponse('{}', content_type='application/json')


def enviar_transmissores(request):
    from .choices import STATUS_TRANSMISSOR_AGUARDANDO
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
    for te in tes:
        dados = enviar(te)
    return HttpResponse('{}', content_type='application/json')


def consultar_transmissores(request):
    from .choices import STATUS_TRANSMISSOR_ENVIADO
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO)
    for te in tes:
        dados = consultar(te)
    return HttpResponse('{}', content_type='application/json')
