from django.core.management.base import BaseCommand

from apps.esocial.choices import STATUS_TRANSMISSOR_AGUARDANDO
from apps.esocial.models import Lotes


class Command(BaseCommand):
    help = 'Enviar eSocial'

    def handle(
            self,
            *args,
            **options):
        trm = Lotes.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
        for tle in trm:
            tle.enviar()
            self.stdout.write(
                '\n{} {} {} {}'.format(
                    tle.id,
                    tle.status,
                    tle.resposta_codigo,
                    tle.resposta_descricao, ))
