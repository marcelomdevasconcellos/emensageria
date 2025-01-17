from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_IMPORTADO, \
    STATUS_TRANSMISSOR_AGUARDANDO, \
    STATUS_TRANSMISSOR_CADASTRADO
from apps.esocial.models import Eventos, Lotes
from config.functions import verify_domain


@login_required
def enviar_transmissores(
        request):
    Lotes.objects.filter(status=STATUS_TRANSMISSOR_CADASTRADO).update(
        status=STATUS_TRANSMISSOR_AGUARDANDO)
    evt = Eventos.objects.filter(status__in=[STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_IMPORTADO])
    for e in evt:
        e.vincular_transmissor()
    tes = Lotes.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO).all()
    for te in tes:
        te.enviar()
    referer = request.META.get('HTTP_REFERER', '')
    if referer and verify_domain(referer):
        messages.success(request, 'Lotes enviados')
        return HttpResponseRedirect(referer)
    return HttpResponse(
        '{"mensagem": "Lotes enviados"}',
        content_type='application/json')
