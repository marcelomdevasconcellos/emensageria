import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos
from config.functions import verify_domain


@login_required
def consultar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    referer = request.META.get('HTTP_REFERER')
    if not evt.lote:
        evt.vincular_transmissor()
    if evt.lote:
        response = evt.lote.consultar()
    else:
        messages.error(
            request,
            "Erro na consulta: transmissor não vinculado ao evento.")
        if referer and verify_domain(referer):
            return HttpResponseRedirect(referer)
        return HttpResponse(
            json.dumps({'error': 'Transmissor não vinculado ao evento'}),
            content_type='application/json')
    if referer and verify_domain(referer):
        return HttpResponseRedirect(referer)
    return HttpResponse(json.dumps(response), content_type='application/json')
