from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from apps.esocial.models import Eventos


@login_required
def visualizar_xml(
        request,
        pk):
    evt = get_object_or_404(Eventos, id=pk)
    if not evt.lote:
        evt.vincular_transmissor()
    evt.create_xml()
    response = HttpResponse(
        evt.evento_xml,
        content_type='text/xml')
    # response['Content-Disposition'] = 'attachment; filename="%s.xml"' % evt.identidade
    return response
