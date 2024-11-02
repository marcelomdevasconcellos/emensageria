import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import TransmissorEventos


@login_required
def consultar_transmissor(
        request,
        pk):
    te = get_object_or_404(TransmissorEventos, id=pk)
    response = te.consultar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')
