import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from apps.esocial.choices import STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO
from apps.esocial.models import Eventos


@login_required
def validar_eventos(
        request):
    evts = Eventos.objects.filter(status__in=[STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO])
    for evt in evts:
        if not evt.transmissor_evento:
            evt.vincular_transmissor()
        evt.create_xml()
        evt.validar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps({}), content_type='application/json')
