from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from apps.esocial.models import Certificados as CertificadosEsocial
from apps.esocial.models import Transmissor as TransmissorEsocial


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        from django.db.models import Q
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if user.is_superuser:
            certificados_esocial = CertificadosEsocial.all_objects. \
                values('id', 'nome')
            transmissores_esocial = TransmissorEsocial.all_objects. \
                values('id', 'nome_empresa', 'tpinsc', 'nrinsc')
        else:
            certificados_esocial = CertificadosEsocial.all_objects. \
                filter(Q(created_by_id=user.id) | Q(users__id=user.id)). \
                values('id', 'nome')
            transmissores_esocial = TransmissorEsocial.all_objects. \
                filter(Q(created_by_id=user.id) | Q(users__id=user.id)). \
                values('id', 'nome_empresa', 'tpinsc', 'nrinsc')

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'esocial': {'certificados': certificados_esocial,
                        'transmissores': transmissores_esocial,
                        },
        })
