from django.core.management.base import BaseCommand
from django.db.models import Q

from ...choices import STATUS_TRANSMISSOR_ENVIADO
from ...models import Lotes


class Command(BaseCommand):
    help = 'Consultar eSocial'

    def handle(self, *args, **options):
        trm = Lotes.objects.filter(
            Q(status=STATUS_TRANSMISSOR_ENVIADO) | Q(
                retorno_consulta__icontains='Código do erro: 301'))
        for tle in trm:
            tle.consultar()
            self.stdout.write('\n{} {} {} {}'.format(
                tle.id,
                tle.status,
                tle.resposta_codigo,
                tle.resposta_descricao, ))
