import django_filters as filters

from apps.transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    account = filters.CharFilter(method='account_transactions')

    class Meta:
        model = Transaction
        fields = ['account', 'category', 'is_completed']

    def account_transactions(self, queryset, name, value):
        if value:
            return queryset.for_account(value)
        return queryset
