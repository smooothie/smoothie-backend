from django.db.models import Q

import django_filters as filters
from graphql_relay import from_global_id

from apps.accounts.models import Account
from apps.transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    account_from = filters.ModelChoiceFilter(queryset=Account.objects.all(),
                                             method='account_transactions')

    class Meta:
        model = Transaction
        fields = ['account_from', 'category', 'is_completed']

    def account_transactions(self, queryset, name, value):
        if value:
            account_id = from_global_id(value)[1]
            return queryset.filter(Q(account_from_id=account_id) | Q(account_to_id=account_id))
        return queryset
