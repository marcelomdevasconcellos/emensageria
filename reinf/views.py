import os
from django.shortcuts import render
from django.http import HttpResponse
from reinf.models import Eventos
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


# Create your views here.

def dashboard_json(request):
    import json
    dashboard_data = {
        'reinf_quant_cadastrados': Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO).count(),
        'reinf_quant_importados': Eventos.objects.filter(status=STATUS_EVENTO_IMPORTADO).count(),
        'reinf_quant_erros_validacao': Eventos.objects.filter(status=STATUS_EVENTO_VALIDADO_ERRO).count(),
        'reinf_quant_validados': Eventos.objects.filter(status=STATUS_EVENTO_VALIDADO).count(),
        'reinf_quant_erros_envio': Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO_ERRO).count(),
        'reinf_quant_enviados': Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO).count(),
        'reinf_quant_processados': Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO).count(),
    }
    return HttpResponse(json.dumps(dashboard_data, indent = 4))