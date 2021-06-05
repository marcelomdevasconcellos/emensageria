from django.core.management.base import BaseCommand
from ...models import TransmissorEventos
from ...choices import STATUS_TRANSMISSOR_AGUARDANDO



class Command(BaseCommand):
    help = 'Enviar Reinf'

    def handle(self, *args, **options):
        trm = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
        for tle in trm:
            tle.enviar()
            self.stdout.write('\n{} {} {} {}'.format(
                tle.id,
                tle.status,
                tle.resposta_codigo,
                tle.resposta_descricao, ))
