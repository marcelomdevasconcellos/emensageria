from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_TRANSMISSOR_ENVIADO
from apps.esocial.models import Lotes
from config.functions import verify_domain


@login_required
def consultar_transmissores(
        request):
    tes = Lotes.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO).all()
    for te in tes:
        te.consultar()
    referer = request.META.get('HTTP_REFERER', '')
    if referer and verify_domain(referer):
        messages.success(request, 'Lotes consultados')
        return HttpResponseRedirect(referer)
    return HttpResponse(
        '{"mensagem": "Lotes consultados"}',
        content_type='application/json')
