from django.db.models import Q

import django_filters as filters
from graphql_relay import from_global_id

from apps.transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    account_from = filters.CharFilter(method='account_transactions')

    class Meta:
        model = Transaction
        fields = ['account_from', 'category', 'is_completed']

    def account_transactions(self, queryset, name, value):
        if value:
            # support both database id and GraphQL global id
            try:
                account_id = int(value)
            except ValueError:
                try:
                    account_id = value if isinstance(value, int) else from_global_id(value)[1]
                except Exception:
                    return queryset.none()
            return queryset.filter(Q(account_from_id=account_id) | Q(account_to_id=account_id))
        return queryset
