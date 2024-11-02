from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_IMPORTADO, \
    STATUS_TRANSMISSOR_AGUARDANDO, \
    STATUS_TRANSMISSOR_CADASTRADO
from apps.esocial.models import Eventos, TransmissorEventos


@login_required
def enviar_transmissores(
        request):
    TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_CADASTRADO).update(
        status=STATUS_TRANSMISSOR_AGUARDANDO)
    evt = Eventos.objects.filter(status__in=[STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_IMPORTADO])
    for e in evt:
        e.vincular_transmissor()
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO).all()
    for te in tes:
        te.enviar()
    if request.META.get('HTTP_REFERER'):
        messages.success(request, 'Lotes enviados')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(
        '{"mensagem": "Lotes enviados"}',
        content_type='application/json')
