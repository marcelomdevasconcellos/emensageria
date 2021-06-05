from django import forms

from .choices import STATUS_EVENTO_CADASTRADO
from .models import Eventos, Certificados, Arquivos


class EventosForm(forms.ModelForm):
    evento_json = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Eventos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventosForm, self).__init__(*args, **kwargs)

        if self.instance.pk and self.instance.status == STATUS_EVENTO_CADASTRADO:
            self.fields['evento'].disabled = True
            self.fields['versao'].disabled = True
            self.fields['operacao'].disabled = True

        if self.instance.pk and self.instance.status != STATUS_EVENTO_CADASTRADO:
            for f in list(self.fields):
                self.fields[f].disabled = True


class CertificadosForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Certificados
        fields = '__all__'


class ArquivosForm(forms.ModelForm):
    class Meta:
        model = Arquivos
        fields = '__all__'
