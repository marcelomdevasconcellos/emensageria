import datetime
from constance import config
from config import settings


def admin_media(request):
    return {
        'hoje': datetime.datetime.today(),
        'DEBUG': settings.DEBUG,
        'DATABASE_NAME': settings.DATABASES['default']['NAME'],
        'get_tags': False,
    }
