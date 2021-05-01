from datetime import datetime

from django import forms
from django.db.models import Q
from django.forms import widgets
from django.core.exceptions import ValidationError

from .models import Eventos, Certificados, Arquivos


class EventosForm(forms.ModelForm):

    evento_json = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Eventos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventosForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['evento'].disabled = True
            self.fields['versao'].disabled = True
            self.fields['operacao'].disabled = True


class CertificadosForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Certificados
        fields = '__all__'


class ArquivosForm(forms.ModelForm):
    class Meta:
        model = Arquivos
        fields = '__all__'
