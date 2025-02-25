import base64
import os
from typing import Any

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.db import models

from config.mixins import BaseModelEsocial

User = get_user_model()


def get_cipher():
    """Retorna uma instância de Fernet para criptografia/descriptografia."""
    return Fernet(settings.CRYPTO_KEY.encode())


class Certificados(BaseModelEsocial):
    cols = {
        'nome': 12,
        'certificado': 12,
        'senha': 12,
        'users': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    nome = models.CharField('Nome', max_length=300, )
    fs_certificado = FileSystemStorage(location=os.path.join(settings.BASE_DIR, settings.CERT_PATH))
    certificado = models.FileField('Arquivo', storage=fs_certificado)
    senha_certificado = models.TextField(
        "Senha do certificado criptografada", null=True, blank=True)
    users: models.ManyToManyField = models.ManyToManyField(
        User, verbose_name='Usuários', related_name='esocial_crt_users', blank=True,
        help_text="Informe a lista de usuários que tem acesso a utilizar este certificado.")

    _senha_certificado_input: Any = None

    def get_senha(
            self):
        return self.get_senha_certificado()

    def cert_pem_file(
            self):
        file = os.path.join(settings.BASE_DIR, settings.CERT_PATH, 'cert_{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def key_pem_file(
            self):
        file = os.path.join(settings.BASE_DIR, settings.CERT_PATH, 'key_{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def cert_host(
            self):
        return os.path.join(settings.BASE_DIR, settings.CERT_PATH, self.certificado.name)

    def capath(
            self):
        return os.path.join(settings.BASE_DIR, 'cacerts', 'esocial')

    def create_pem_files(
            self):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.serialization import pkcs12
        from cryptography.hazmat.backends import default_backend

        import os

        pkcs12_path = self.cert_host()
        senha = self.get_senha().encode()  # Certifique-se de que a senha está em bytes

        try:
            with open(pkcs12_path, 'rb') as pkcs12_file:
                pkcs12_data = pkcs12_file.read()
                pkcs12_obj = pkcs12.load_key_and_certificates(pkcs12_data, senha, default_backend())
        except Exception as e:
            raise ValueError(f"Erro ao carregar o arquivo PKCS12: {e}")

        # Extrair a chave privada e o certificado
        try:
            private_key = pkcs12_obj[0]
            certificate = pkcs12_obj[1]

            key_str = private_key.private_bytes(  # type: ignore
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            cert_str = certificate.public_bytes(  # type: ignore
                serialization.Encoding.PEM)
        except Exception as e:
            raise ValueError(f"Erro ao extrair a chave ou o certificado: {e}")

        # Salvar os arquivos PEM
        cert_pem_path = self.cert_pem_file()
        key_pem_path = self.key_pem_file()

        if not os.path.isfile(cert_pem_path):
            try:
                with open(cert_pem_path, 'wb') as cert_pem_file:
                    cert_pem_file.write(cert_str)
            except Exception as e:
                raise ValueError(f"Erro ao salvar o arquivo cert PEM: {e}")

        if not os.path.isfile(key_pem_path):
            try:
                with open(key_pem_path, 'wb') as key_pem_file:
                    key_pem_file.write(key_str)
            except Exception as e:
                raise ValueError(f"Erro ao salvar o arquivo key PEM: {e}")

        return {
            'key_str': key_str,
            'cert_str': cert_str,
        }

    def save(
            self,
            *args,
            **kwargs):
        # A senha será criptografada apenas se um novo valor for fornecido
        if self._senha_certificado_input:
            self.senha_certificado = base64.urlsafe_b64encode(
                get_cipher().encrypt(self._senha_certificado_input.encode())
            ).decode()  # Criptografa e armazena em base64
        super().save(*args, **kwargs)

    def get_senha_certificado(
            self):
        """Descriptografa e retorna a senha do certificado."""
        if self.senha_certificado:
            try:
                return get_cipher().decrypt(
                    base64.urlsafe_b64decode(self.senha_certificado.encode())).decode()
            except Exception:
                return None
        return None

    def __str__(
            self):
        return self.nome

    class Meta:
        verbose_name = 'Certificados'
        verbose_name_plural = 'Certificados'
        ordering = [
            '-id', ]
