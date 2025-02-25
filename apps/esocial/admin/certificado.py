from django.contrib import admin, messages

from apps.esocial.forms.certificado import CertificadosForm
from apps.esocial.models import Certificados
from config.mixins import AuditoriaAdminEventos


@admin.register(Certificados)
class CertificadosAdmin(AuditoriaAdminEventos):
    form = CertificadosForm
    search_fields = (
        'nome',)
    list_display = (
        'id', 'nome',)
    fieldsets = ((None, {
        'fields': ('nome', 'certificado', 'senha_certificado_input',)
    }),)

    def get_fieldsets(
            self,
            request,
            obj=None):
        fieldsets = super(CertificadosAdmin, self).get_fieldsets(request, obj)
        if request.user.has_perm('auth.view_user'):
            return ((None, {
                'fields': ('nome', 'certificado', 'senha_certificado_input',)
            }), ('Usuários', {
                'fields': ('users',)
            }))
        return fieldsets

    def save_model(
            self,
            request,
            obj,
            form,
            change):
        super().save_model(request, obj, form, change)
        try:
            obj.create_pem_files()
        except Exception as e:
            messages.error(
                request, 'Erro ao tentar criar as chaves do certificado, '
                         'verifique se o mesmo está com a senha correta. {}'.format(e))
