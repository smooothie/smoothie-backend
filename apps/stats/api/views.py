from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.stats.filters import TransactionsFilter
from apps.transactions.models import Transaction
from .serializers import DynamicsSerializer, StructureSerializer


class StructureViewSet(ListModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = StructureSerializer
    pagination_class = None
    filterset_class = TransactionsFilter

    def get_queryset(self):
        account_type = self.kwargs.get('account_type')
        qs = super().get_queryset().filter(account_from__user=self.request.user)
        if account_type == 'income':
            qs = qs.filter(account_from__item_type='incomebalance')
        elif account_type == 'spending':
            qs = qs.filter(account_to__item_type='spendingbalance')
        return qs

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).categories_structure()


class DynamicsViewSet(ListModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = DynamicsSerializer
    pagination_class = None
    filterset_class = TransactionsFilter

    def get_queryset(self):
        account_type = self.kwargs.get('account_type')
        qs = super().get_queryset().filter(account_from__user=self.request.user)
        if account_type == 'income':
            qs = qs.filter(account_from__item_type='incomebalance')
        elif account_type == 'spending':
            qs = qs.filter(account_to__item_type='spendingbalance')
        return qs

    def filter_queryset(self, queryset):
        kwargs = {}
        period = self.request.query_params.get('period')
        if period is not None:
            kwargs['period'] = period
        return super().filter_queryset(queryset).dynamics(**kwargs)
