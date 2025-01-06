import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos


@login_required
def enviar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    response = evt.enviar()
    referer = request.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts=None):
        return HttpResponseRedirect(referer)
    return HttpResponse(json.dumps(response), content_type='application/json')
    return HttpResponse(json.dumps(response), content_type='application/json')
