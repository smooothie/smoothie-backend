from django.db.models import Q

import django_filters as filters

from apps.transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    account = filters.CharFilter(method='account_transactions')

    class Meta:
        model = Transaction
        fields = ['account', 'category', 'is_completed']

    def account_transactions(self, queryset, name, value):
        if value:
            return queryset.filter(Q(account_from_id=value) | Q(account_to_id=value))
        return queryset
