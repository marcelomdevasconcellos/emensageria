import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import Lotes
from config.functions import verify_domain


@login_required
def consultar_transmissor(
        request,
        pk):
    te = get_object_or_404(Lotes, id=pk)
    response = te.consultar()
    referer = request.META.get('HTTP_REFERER', '')
    if referer and verify_domain(referer):
        return HttpResponseRedirect(referer)
    return HttpResponse(json.dumps(response), content_type='application/json')
