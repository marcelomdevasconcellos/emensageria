"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import environ  # type: ignore
from django.utils.log import DEFAULT_LOGGING as LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    env('ALLOWED_HOSTS'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'adminlteui',
    'adminlteui_custom',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.esocial.apps.esocialConfig',
    'apps.users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'adminlteui_custom', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'constance.context_processors.config',
                'config.context_processors.admin_media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DECIMAL_SEPARATOR = ','

THOUSAND_SEPARATOR = '.'

USE_THOUSAND_SEPARATOR = True

LINK_WEBSITE = env('LINK_WEBSITE', default='')

# Configurações de Versão do Aplicativo
VERSAO_EMENSAGERIA = '2.0.4'
VERSAO_LAYOUT_ESOCIAL = env('VERSAO_LAYOUT_ESOCIAL', default='v_S_01_03_00')
ESOCIAL_TPAMB = env('ESOCIAL_TPAMB', default='2')

# Targets: tests, production
if ESOCIAL_TPAMB == '1':
    ESOCIAL_TARGET = 'production'
else:
    ESOCIAL_TARGET = 'tests'

ESOCIAL_PROCEMI = env('ESOCIAL_PROCEMI', default='1')

VERSOES_ESOCIAL = [
    'v_S_01_00_00',
    'v_S_01_01_00',
    'v_S_01_02_00',
    'v_S_01_03_00', ]

# Configurações para o envio de emails
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default="[eMensageriaOpenSource] ")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('SERVER_EMAIL', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
SERVER_EMAIL = env('SERVER_EMAIL', default='')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')

AUTH_USER_MODEL = "users.User"

LOG_FILENAME = "emensageria.log"
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)  # Cria o diretório de logs, caso não exista


# Função para processar a variável ADMINS
def parse_admins(
        admins_string):
    if not admins_string:
        return []
    admins = []
    for admin in admins_string.split(";"):
        if admin.strip():
            name, email = admin.split(",")
            admins.append((name.strip(), email.strip()))
    return admins


ADMINS = parse_admins(
    env('ADMINS', default='Marcelo Vasconcellos, marcelomdevasconcellos@gmail.com;'))

LOGGING['handlers']['mail_admins']['include_html'] = True

SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

# caminho dos certificados
CERT_PATH = env('CERT_PATH', default='certificados/')

# Somente no Windows Server
# caminho do CURL
# Necessário baixar o curl para windows no endereço: https://curl.se/windows/
CURL_PATH = env('CURL_PATH', default='')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(env('STATIC_ROOT', default='static'))
STATIC_URL = env('STATIC_URL', default='/static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, env('MEDIA_ROOT', default='media'))
MEDIA_URL = env('MEDIA_URL', default='/media/')

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAdminUser',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    )
}

ADMINLTE_CONFIG_CLASS = 'adminlteui_custom.adminlte_config.MyAdminlteConfig'

# Visualiza manual do sistema no menu.
SYSTEM_MANUAL_SHOW_IN_MENU = env('SYSTEM_MANUAL_SHOW_IN_MENU', default=False)

# Link do manual do sistema.
SYSTEM_MANUAL_LINK = env('SYSTEM_MANUAL_LINK', default='#')

# Caminho relativo do local aonde serão armazenados os arquivos.
# Insira "/" no início para definir diretórios absolutos.
FILES_PATH = env('MEDIA_ROOT', default=os.path.join(MEDIA_ROOT, 'arquivos'))
os.makedirs(os.path.join(FILES_PATH), exist_ok=True)  # Cria o diretório de logs, caso não exista

os.makedirs(os.path.join(FILES_PATH, "comunicacao", "WsConsultarLoteEventos"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "comunicacao", "WsEnviarLoteEventos"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "esocial", "importacao", "aguardando"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "esocial", "importacao", "erro"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "esocial", "importacao", "processado"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "esocial", "importacao", "processando"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "esocial", "importacao", "temp"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "eventos", "esocial"), exist_ok=True)
os.makedirs(os.path.join(FILES_PATH, "recibos", "esocial"), exist_ok=True)

# Cada usuário pode ver somente os que ele mesmo cadastrou.
# Os Super-usuários vêem todos os eventos.
FILTER_BY_USER = env('FILTER_BY_USER', default=False)

# Visualiza imagem do logotipo na tela de Login.
LOGO_IMAGE_IN_LOGIN = env('LOGO_IMAGE_IN_LOGIN', default=False)

# Logotipo da empresa
LOGO_IMAGE = env('LOGO_IMAGE', default='')

# Nome da empresa que está disponibilizando o sistema
REPRESENTANTE_NOME = env('REPRESENTANTE_NOME', default='EMENSAGERIA')

# Contrato da central de serviços
REPRESENTANTE_CENTRAL_SERVICOS = env(
    'REPRESENTANTE_CENTRAL_SERVICOS',
    default='Central de Serviços (99) 99999.9999')

# Token de autenticação do sistema para acesso aos webservices
SYSTEM_TOKEN_SCHEDULE = env(
    'SYSTEM_TOKEN_SCHEDULE',
    default='9944b09199c62bcf9418ad846dd0123e4bbdfc6ee4b')

# Tempo entre validações (em minutos) dos eventos do eSocial.
ESOCIAL_VALIDATE_RUN_EVERY_MINS = env('ESOCIAL_VALIDATE_RUN_EVERY_MINS', default=10)

# Tempo entre envios (em minutos) dos eventos do eSocial.'
ESOCIAL_SEND_RUN_EVERY_MINS = env('ESOCIAL_SEND_RUN_EVERY_MINS', default=10)

# Tempo entre consultas (em minutos) dos eventos do eSocial.
ESOCIAL_CONSULT_RUN_EVERY_MINS = env('ESOCIAL_CONSULT_RUN_EVERY_MINS', default=10)

# Quantidade do mínima do lote do eSocial.
ESOCIAL_LOTE_MIN = env('ESOCIAL_LOTE_MIN', default=1)

# Quantidade do máxima do lote do eSocial.
ESOCIAL_LOTE_MAX = env('ESOCIAL_LOTE_MAX', default=60)

# Timeout do eSocial.
ESOCIAL_TIMEOUT = env('ESOCIAL_TIMEOUT', default=3600)

# Envio automático do eSocial.
ESOCIAL_AUTOMATIC_FUNCTIONS_ENABLED = env(
    'ESOCIAL_AUTOMATIC_FUNCTIONS_ENABLED', default=False)

# Caminho completo do Certificado do SERPRO para o eSocial'
ESOCIAL_CA_CERT_PEM_FILE = env(
    'ESOCIAL_CA_CERT_PEM_FILE',
    default='certificado/webservicesproducaorestritaesocialgovbr.crt')

# Tipo de ambiente padrão do sistema do eSocial.'
ESOCIAL_TP_AMB = env('ESOCIAL_TP_AMB', default='Produção Restrita')

# Força o sistema para envio pelo ambiente produção restrita do eSocial.'
ESOCIAL_FORCE_PRODUCAO_RESTRITA = env(
    'ESOCIAL_FORCE_PRODUCAO_RESTRITA', default=True)

# Ativa a função de verificar predecessão antes dos envios dos eventos do eSocial.'
ESOCIAL_VERIFICAR_PREDECESSAO_ANTES_ENVIO = env(
    'ESOCIAL_VERIFICAR_PREDECESSAO_ANTES_ENVIO', default=False)

# Tempo de leitura de arquivos importados (em minutos).'
IMPORT_FILES_RUN_EVERY_MINS = env(
    'IMPORT_FILES_RUN_EVERY_MINS', default=10)

# Quantidade do lote de arquivos de eventos para importação.'
IMPORT_LEN_EVENTS = env(
    'IMPORT_LEN_EVENTS', default=10)

# Funções de importação automáticas ativadas.
IMPORT_AUTOMATIC_FUNCTIONS_ENABLED = env(
    'IMPORT_AUTOMATIC_FUNCTIONS_ENABLED', default=False)

# Tempo entre validações (em minutos) dos eventos do EFD-Reinf.'
EFDREINF_VALIDADE_RUN_EVERY_MINS = env(
    'EFDREINF_VALIDADE_RUN_EVERY_MINS', default=10)

# Tempo entre envios (em minutos) dos eventos do EFD-Reinf.'
EFDREINF_SEND_RUN_EVERY_MINS = env(
    'EFDREINF_SEND_RUN_EVERY_MINS', default=10)

# Tempo entre consultas (em minutos) dos eventos do EFD-Reinf.'
EFDREINF_CONSULT_RUN_EVERY_MINS = env(
    'EFDREINF_CONSULT_RUN_EVERY_MINS', default=10)

# Caminho completo do Certificado do SERPRO para o EFD-Reinf'
EFDREINF_CA_CERT_PEM_FILE = env(
    'EFDREINF_CA_CERT_PEM_FILE', default='certificados/acserproacfv5.crt')

# Quantidade do mínima do lote do EFD-Reinf.
EFDREINF_LOTE_MIN = env(
    'EFDREINF_LOTE_MIN', default=1)

# Quantidade do máxima do lote do EFD-Reinf.
EFDREINF_LOTE_MAX = env(
    'EFDREINF_LOTE_MAX', default=60)

# Timeout do EFD-Reinf.
EFDREINF_TIMEOUT = env(
    'EFDREINF_TIMEOUT', default=3600)

# Envio automático do EFD-Reinf.
EFDREINF_AUTOMATIC_FUNCTIONS_ENABLED = env(
    'EFDREINF_AUTOMATIC_FUNCTIONS_ENABLED', default=False)

# Tipo de ambiente padrão do sistema do EFD-Reinf.
EFDREINF_TP_AMB = env(
    'EFDREINF_TP_AMB', default='Produção Restrita')

# Força o sistema para envio pelo ambiente produção restrita do EFD-Reinf.
EFDREINF_FORCE_PRODUCAO_RESTRITA = env(
    'EFDREINF_FORCE_PRODUCAO_RESTRITA', default=True)

# Ativa a função de verificar predecessão antes dos envios dos eventos do EFD-Reinf.
EFDREINF_VERIFICAR_PREDECESSAO_ANTES_ENVIO = env(
    'EFDREINF_VERIFICAR_PREDECESSAO_ANTES_ENVIO', default=False)

# E-mail de recuperação de senha.
EMAIL_RECUPERACAO_SENHA = env(
    'EMAIL_RECUPERACAO_SENHA', default='emensageria@emensageria.com.br')

# Assunto padrão do e-mail de recuperação de senha.
EMAIL_RECUPERACAO_SENHA_ASSUNTO = env(
    'EMAIL_RECUPERACAO_SENHA_ASSUNTO', default='Criação/Recuperação de senha | eMensageria')

# Mensagem padrão do e-mail de recuperação de senha.
EMAIL_RECUPERACAO_SENHA_MENSAGEM = env(
    'EMAIL_RECUPERACAO_SENHA_MENSAGEM',
    default='<p>Prezado %(nome)s,<br>Acesse o sistema pelo link '
            '<a href="%(endereco)s">eMensageriaOpenSource</a><br>Utilizando '
            'o usuário: <strong>%(usuario)s</strong><br>Senha: '
            '<strong>%(senha)s</strong><br>E-mail gerado '
            'automaticamente pelo sistema eMensageria</p>')

CRYPTO_KEY = env('CRYPTO_KEY')
