from django.db.models import Q

from rest_framework import viewsets

from apps.transactions.models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = {
        'date': 'date',
    }
    default_ordering = ('-date',)
    filterset_fields = ['category', 'is_completed']

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
            Q(account_from__user=user) |
            Q(account_to__user=user)
        )
