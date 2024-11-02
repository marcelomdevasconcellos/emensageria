# Generated by Django 4.2.17 on 2025-01-02 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esocial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transmissoreventos',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transmissoreventos',
            name='transmissor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_transmissor', to='esocial.transmissor', verbose_name='Transmissor'),
        ),
        migrations.AddField(
            model_name='transmissoreventos',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transmissor',
            name='certificado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_certificado', to='esocial.certificados', verbose_name='Certificado'),
        ),
        migrations.AddField(
            model_name='transmissor',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transmissor',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transmissor',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Informe a lista de usuários que tem acesso a utilizar este transmissor.', related_name='transmissores_users', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='certificado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='certificado_esocial_historico', to='esocial.certificados', verbose_name='Certificado'),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='evt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evento_esocial', to='esocial.eventos', verbose_name='Evento'),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='transmissor_evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transmissor_esocial_historico', to='esocial.transmissoreventos', verbose_name='Transmissor'),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='transmissor_evento_error',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_transmissor_eventos_erros_historico', to='esocial.transmissoreventos', verbose_name='Transmissores (Erro)'),
        ),
        migrations.AddField(
            model_name='eventoshistorico',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventos',
            name='certificado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='certificado_esocial', to='esocial.certificados', verbose_name='Certificado'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventos',
            name='transmissor_evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transmissor_esocial', to='esocial.transmissoreventos', verbose_name='Lote/Transmissor'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='transmissor_evento_error',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_transmissor_eventos_erros', to='esocial.transmissoreventos', verbose_name='Lote/Transmissor (Erro)'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='certificados',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='certificados',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated_by_esocial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='certificados',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Informe a lista de usuários que tem acesso a utilizar este certificado.', related_name='esocial_crt_users', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
    ]
