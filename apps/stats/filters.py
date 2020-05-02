import django_filters as filters

from apps.transactions.models import Transaction


class TransactionsFilter(filters.FilterSet):
    currency = filters.CharFilter(field_name='amount_currency')
    date_from = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['currency', 'date_from', 'date_to']
