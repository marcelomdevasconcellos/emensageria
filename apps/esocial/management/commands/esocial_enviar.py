from django.core.management.base import BaseCommand

from apps.esocial.choices import STATUS_TRANSMISSOR_AGUARDANDO
from apps.esocial.models import TransmissorEventos


class Command(BaseCommand):
    help = 'Enviar eSocial'

    def handle(
            self,
            *args,
            **options):
        trm = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
        for tle in trm:
            tle.enviar()
            self.stdout.write(
                '\n{} {} {} {}'.format(
                    tle.id,
                    tle.status,
                    tle.resposta_codigo,
                    tle.resposta_descricao, ))
