import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO
from apps.esocial.models import Eventos
from config.functions import verify_domain


@login_required
def validar_eventos(
        request):
    evts = Eventos.objects.filter(status__in=[STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO])
    for evt in evts:
        if not evt.lote:
            evt.vincular_transmissor()
        evt.create_xml()
        evt.validar()
    referer = request.META.get('HTTP_REFERER', '')
    if referer and verify_domain(referer):
        return HttpResponseRedirect(referer)
    return HttpResponse(json.dumps({}), content_type='application/json')
