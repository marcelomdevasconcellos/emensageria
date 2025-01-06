import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme

from apps.esocial.choices import STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO
from apps.esocial.models import Eventos


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
    if url_has_allowed_host_and_scheme(referer, allowed_hosts=None):
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect('/')
    return HttpResponse(json.dumps({}), content_type='application/json')
