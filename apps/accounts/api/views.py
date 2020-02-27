from rest_framework import viewsets

from apps.accounts.models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.exclude(item_type__in=['incomebalance', 'spendingbalance'])
    serializer_class = AccountSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
