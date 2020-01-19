import django_filters as filters

from apps.accounts.models import Account


class AccountFilter(filters.FilterSet):
    account_type = filters.CharFilter(method='visible_accounts')

    class Meta:
        model = Account
        fields = ['account_type']

    def visible_accounts(self, queryset, name, value):
        if value == 'visible':
            return queryset.exclude(account_type__in=['incomebalance', 'spendingbalance'])
        return queryset.filter(*{name: value})
