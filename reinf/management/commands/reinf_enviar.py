from django.core.management.base import BaseCommand, CommandError
from reinf.models import TransmissorEventos, Eventos, TransmissorEventosArquivos
import requests
from reinf.functions import create_pem_files, save_file, read_file
from constance import config
import time
from config.settings import BASE_DIR
from reinf.transmissor import enviar
from reinf.choices import STATUS_TRANSMISSOR_AGUARDANDO



class Command(BaseCommand):
    help = 'Enviar eSocial'

    # def add_arguments(self, parser):
    #     parser.add_argument('quant', nargs='+', type=int)

    def handle(self, *args, **options):

        trm = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
        for tle in trm:
            retorno = enviar(tle)
            retorno['id'] = tle.id
            self.stdout.write('\n%(id)s %(status)s: %(mensagem)s' % retorno)
