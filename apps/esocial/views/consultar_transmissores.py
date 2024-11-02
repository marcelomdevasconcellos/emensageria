from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_TRANSMISSOR_ENVIADO
from apps.esocial.models import TransmissorEventos


@login_required
def consultar_transmissores(
        request):
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO).all()
    for te in tes:
        te.consultar()
    if request.META.get('HTTP_REFERER'):
        messages.success(request, 'Lotes consultados')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(
        '{"mensagem": "Lotes consultados"}',
        content_type='application/json')
