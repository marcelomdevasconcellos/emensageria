from django_filters import rest_framework as filters

from ..models import (
    Eventos,
)


class EventosFilter(filters.FilterSet):
    class Meta:
        model = Eventos
        fields = {
            'identidade': ['exact'], }
