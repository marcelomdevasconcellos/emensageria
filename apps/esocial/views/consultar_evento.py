import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from apps.esocial.models import Eventos

@login_required
def consultar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    if not evt.lote:
        evt.vincular_transmissor()
    if evt.lote:
        response = evt.lote.consultar()
    else:
        messages.error(
            request,
            "Erro na consulta: transmissor não vinculado ao evento.")
        referer = request.META.get('HTTP_REFERER')
        if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts=None):
            return HttpResponseRedirect(referer)
        return HttpResponse(
            json.dumps({'error': 'Transmissor não vinculado ao evento'}),
            content_type='application/json')
    referer = request.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts=None):
        return HttpResponseRedirect(referer)
    return HttpResponse(json.dumps(response), content_type='application/json')
