from django import forms

from apps.esocial.models import Certificados


class CertificadosForm(forms.ModelForm):
    senha_certificado_input = forms.CharField(
        label="Senha do certificado",
        required=False, widget=forms.PasswordInput
    )

    class Meta:
        model = Certificados
        fields = ['nome', 'certificado',
                  'senha_certificado_input', 'users', ]

    def save(self, commit=True):
        # Criptografa a senha se o campo tiver sido preenchido
        instance = super().save(commit=False)
        senha = self.cleaned_data.get('senha_certificado_input')
        if senha:  # Só salva a senha se o campo for preenchido
            instance._senha_certificado_input = senha
        if commit:
            instance.save()
        return instance
