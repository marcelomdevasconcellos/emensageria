from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from apps.esocial.models import Eventos


@login_required
def validar_evento(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    if evt.evento_json:
        if not evt.lote:
            evt = evt.vincular_transmissor()
            evt = Eventos.objects.get(id=pk)
            # print(evt.lote)
        evt.create_xml()
        evt.validar()
    else:
        messages.add_message(
            request, messages.ERROR,
            f'Não é possível validar pois o evento {evt.identidade} não possui dados suficientes!')
    referer = request.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts=None):
        return HttpResponseRedirect(referer)
    return HttpResponse('{}', content_type='application/json')
