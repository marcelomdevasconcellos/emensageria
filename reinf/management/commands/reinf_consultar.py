from django.core.management.base import BaseCommand, CommandError
from reinf.models import TransmissorEventos, Eventos, TransmissorEventosArquivos
import requests
from reinf.functions import create_pem_files, save_file, read_file
from reinf.transmissor import consultar
from constance import config
import time
from config.settings import BASE_DIR
from reinf.choices import STATUS_TRANSMISSOR_ENVIADO


class Command(BaseCommand):
    help = 'Consultar eSocial'

    def handle(self, *args, **options):

        trm = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO)
        for tle in trm:
            retorno = consultar(tle)
            retorno['id'] = tle.id
            self.stdout.write('\n%(id)s %(status)s: %(mensagem)s' % retorno)
            
