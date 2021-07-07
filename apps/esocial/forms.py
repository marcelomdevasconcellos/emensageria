from constance import config
from django import forms
from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_user

from .models import Eventos, Certificados, Arquivos, Transmissor


class EventosForm(forms.ModelForm):
    evento_json = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Eventos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventosForm, self).__init__(*args, **kwargs)
        self.fields['tpamb'].disabled = True
        self.fields['procemi'].disabled = True
        self.fields['verproc'].disabled = True

        if self.instance.pk:
            self.fields['evento'].disabled = True
            self.fields['versao'].disabled = True
            self.fields['operacao'].disabled = True

        if self.instance.pk and not self.instance.is_aberto:
            for f in list(self.fields):
                self.fields[f].disabled = True


class CertificadosForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Certificados
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CertificadosForm, self).__init__(*args, **kwargs)
        current_user = get_current_user()
        if current_user and current_user.has_perm('auth.view_user') and self.fields.get('users'):
            self.fields['users'].widget.attrs['readonly'] = True


class ArquivosForm(forms.ModelForm):
    class Meta:
        model = Arquivos
        fields = '__all__'


class TransmissorForm(forms.ModelForm):
    class Meta:
        model = Transmissor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        nrinsc = cleaned_data.get("nrinsc")
        if config.FILTER_BY_USER:
            current_user = get_current_user()
            transmissores = Transmissor.all_objects.\
                filter(nrinsc=nrinsc).\
                exclude(created_by=current_user).\
                exclude(users__id=current_user.id).all()
            if transmissores:
                raise ValidationError("Já existe um transmissor cadastrado com este número. Entre em contato com o administrador do sistema e solicite que vincule ele ao seu usuário.")

    def __init__(self, *args, **kwargs):
        super(TransmissorForm, self).__init__(*args, **kwargs)
        current_user = get_current_user()
        if current_user and current_user.has_perm('auth.view_user') and self.fields.get('users'):
            self.fields['users'].widget.attrs['readonly'] = True
