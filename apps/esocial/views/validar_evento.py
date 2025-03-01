from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos
from config.functions import verify_domain


@login_required
def validar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    if evt.evento_json:
        if not evt.lote:
            evt.vincular_transmissor()
            evt = Eventos.objects.get(id=pk)
        evt.validar()
    else:
        messages.add_message(
            request, messages.ERROR,
            f'Não é possível validar pois o evento {evt.identidade} não possui dados suficientes!')
    referer = request.META.get('HTTP_REFERER')
    if referer and verify_domain(referer):
        return HttpResponseRedirect(referer)
    return HttpResponse('{}', content_type='application/json')
