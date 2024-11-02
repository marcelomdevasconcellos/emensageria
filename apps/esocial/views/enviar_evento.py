import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos


@login_required
def enviar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    response = evt.enviar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')
