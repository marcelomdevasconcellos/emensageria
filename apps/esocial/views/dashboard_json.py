from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.esocial.choices import STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_CADASTRADO, \
    STATUS_EVENTO_ENVIADO, STATUS_EVENTO_ERRO, \
    STATUS_EVENTO_IMPORTADO, STATUS_EVENTO_PROCESSADO
from apps.esocial.models import Eventos


@login_required
def dashboard_json(
        request):
    import json
    eventos_importados = Eventos.objects.filter(status=STATUS_EVENTO_IMPORTADO)
    eventos_cadastrados = Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO)
    eventos_erros = Eventos.objects.filter(status=STATUS_EVENTO_ERRO)
    eventos_validados = Eventos.objects.filter(status__in=(STATUS_EVENTO_AGUARD_ENVIO,))
    eventos_enviados = Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO)
    eventos_processados = Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO)
    dashboars_data = {
        'esocial_quant_cadastrados': eventos_cadastrados.count(),
        'esocial_quant_erros': eventos_erros.count(),
        'esocial_quant_importados': eventos_importados.count(),
        'esocial_quant_validados': eventos_validados.count(),
        'esocial_quant_enviados': eventos_enviados.count(),
        'esocial_quant_processados': eventos_processados.count(),
        'esocial_cadastrados': list(eventos_cadastrados.values('id', 'evento', 'identidade')),
        'esocial_erros': list(eventos_erros.values('id', 'evento', 'identidade')),
        'esocial_validados': list(eventos_validados.values('id', 'evento', 'identidade')),
        'esocial_importados': list(eventos_importados.values('id', 'evento', 'identidade')),
        'esocial_enviados': list(eventos_enviados.values('id', 'evento', 'identidade')),
        'esocial_processados': list(eventos_processados.values('id', 'evento', 'identidade')),
    }
    return HttpResponse(json.dumps(dashboars_data, indent=4))
