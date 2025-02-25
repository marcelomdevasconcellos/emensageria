from django.contrib import admin

from apps.esocial.forms.transmissor import TransmissorForm
from apps.esocial.models import Transmissor
from config.mixins import AuditoriaAdminEventos


@admin.register(Transmissor)
class TransmissorAdmin(AuditoriaAdminEventos):
    search_fields = (
        'transmissor_tpinsc',
        'transmissor_nrinsc',
        'nome_empresa',
        'nrinsc',
        'tpinsc',)
    list_filter = ()
    list_display = (
        'id',
        'transmissor_tpinsc',
        'transmissor_nrinsc',
        'nome_empresa',
        'nrinsc',
        'tpinsc',
        'certificado',
    )
    fieldsets = (('Transmissor', {
        'fields': ('transmissor_tpinsc', 'transmissor_nrinsc',)
    }), ('Empregador', {
        'fields': ('nome_empresa', 'logotipo', 'endereco_completo',
                   'tpinsc', 'nrinsc', 'certificado')
    }),)
    form = TransmissorForm

    def get_fieldsets(
            self,
            request,
            obj=None):
        fieldsets = super(TransmissorAdmin, self).get_fieldsets(request, obj)
        if request.user.has_perm('auth.view_user'):
            return (('Transmissor', {
                'fields': ('transmissor_tpinsc', 'transmissor_nrinsc',)
            }), ('Empregador', {
                'fields': ('nome_empresa', 'logotipo', 'endereco_completo',
                           'tpinsc', 'nrinsc', 'certificado')
            }), ('Usuários', {
                'fields': ('users',)
            }))
        return fieldsets
