import datetime
from constance import config
from config import settings
from apps.esocial.choices import (
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_VALIDADO_ERRO,
    STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_ENVIADO,
    STATUS_EVENTO_ENVIADO_ERRO,
    STATUS_EVENTO_PROCESSADO,
)


def admin_media(request):
    return {
        'hoje': datetime.datetime.today(),
        'DEBUG': settings.DEBUG,
        'DATABASE_NAME': settings.DATABASES['default']['NAME'],
        'get_tags': False,
        'STATUS_EVENTO_CADASTRADO': STATUS_EVENTO_CADASTRADO,
        'STATUS_EVENTO_VALIDADO_ERRO': STATUS_EVENTO_VALIDADO_ERRO,
        'STATUS_EVENTO_AGUARD_ENVIO': STATUS_EVENTO_AGUARD_ENVIO,
        'STATUS_EVENTO_ENVIADO': STATUS_EVENTO_ENVIADO,
        'STATUS_EVENTO_ENVIADO_ERRO': STATUS_EVENTO_ENVIADO_ERRO,
        'STATUS_EVENTO_PROCESSADO': STATUS_EVENTO_PROCESSADO,
    }
