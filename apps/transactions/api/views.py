from django.db.models import OuterRef

from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from apps.common.expressions import CountSubquery
from apps.transactions.filters import TransactionFilter
from apps.transactions.models import Transaction, TransactionCategory
from .serializers import TransactionCategorySerializer, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = {
        'date': 'date',
    }
    ordering = ('-date',)
    filterset_class = TransactionFilter

    def get_queryset(self):
        return super().get_queryset().for_user(self.request.user.id)


class CategoryAutocompleteViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    search_fields = ['name']
    ordering_fields = {'name': 'name', 'transactions_count': 'transactions_count'}
    ordering = ('-transactions_count', 'name',)

    def get_queryset(self):
        transactions = Transaction.objects.for_user(self.request.user.id)\
            .filter(category=OuterRef('pk'))
        return super().get_queryset().annotate(
            transactions_count=CountSubquery(transactions.values('id')))
