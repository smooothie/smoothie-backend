from django.db.models import Q

from rest_framework import viewsets

from apps.transactions.filters import TransactionFilter
from apps.transactions.models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = {
        'date': 'date',
    }
    ordering = ('-date',)
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
            Q(account_from__user=user) |
            Q(account_to__user=user)
        )
