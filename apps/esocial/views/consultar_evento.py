import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos


@login_required
def consultar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    if not evt.transmissor_evento:
        evt.vincular_transmissor()
    if evt.transmissor_evento:
        response = evt.transmissor_evento.consultar()
    else:
        messages.error(
            request,
            "Erro na consulta: transmissor não vinculado ao evento.")
        if request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponse(
            json.dumps({'error': 'Transmissor não vinculado ao evento'}),
            content_type='application/json')
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')
