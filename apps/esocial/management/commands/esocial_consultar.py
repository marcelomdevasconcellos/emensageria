from django.core.management.base import BaseCommand
from ...choices import STATUS_TRANSMISSOR_ENVIADO
from ...models import Lotes


class Command(BaseCommand):
    help = 'Consultar eSocial'

    def handle(self, *args, **options):
        trm = Lotes.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO)
        for tle in trm:
            tle.consultar()
            self.stdout.write('\n{} {} {} {}'.format(
                tle.id,
                tle.status,
                tle.resposta_codigo,
                tle.resposta_descricao, ))
