import datetime

from apps.esocial.choices import (
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_IMPORTADO,
    STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_ENVIADO,
    STATUS_EVENTO_ERRO,
    STATUS_EVENTO_PROCESSADO,
)
from config import settings


def admin_media(request):
    return {
        'hoje': datetime.datetime.today(),
        'DEBUG': settings.DEBUG,
        'VERSAO_EMENSAGERIA': settings.VERSAO_EMENSAGERIA,
        'DATABASE_NAME': settings.DATABASES['default']['NAME'],
        'get_tags': False,
        'MEDIA_URL': settings.MEDIA_URL,
        'LINK_WEBSITE': settings.LINK_WEBSITE,
        'STATUS_EVENTO_CADASTRADO': STATUS_EVENTO_CADASTRADO,
        'STATUS_EVENTO_IMPORTADO': STATUS_EVENTO_IMPORTADO,
        'STATUS_EVENTO_AGUARD_ENVIO': STATUS_EVENTO_AGUARD_ENVIO,
        'STATUS_EVENTO_ENVIADO': STATUS_EVENTO_ENVIADO,
        'STATUS_EVENTO_ERRO': STATUS_EVENTO_ERRO,
        'STATUS_EVENTO_PROCESSADO': STATUS_EVENTO_PROCESSADO,
    }
