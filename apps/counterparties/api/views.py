from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.counterparties.models import Counterparty
from .serializers import SimpleCounterpartySerializer


class CounterpartyAutocompleteViewSet(ListModelMixin, GenericViewSet):
    queryset = Counterparty.objects.all()
    serializer_class = SimpleCounterpartySerializer
    search_fields = ['name']
    ordering_fields = {'name': 'name'}
    ordering = ('name',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
