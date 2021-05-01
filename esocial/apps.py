from django.apps import AppConfig


class EsocialConfig(AppConfig):
    name = 'esocial'
    verbose_name = 'eSocial'

    def icon(self):
        return 'fa-circle'
