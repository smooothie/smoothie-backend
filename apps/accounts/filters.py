import django_filters as filters

from apps.accounts.models import Account


class AccountFilter(filters.FilterSet):
    item_type = filters.CharFilter(method='visible_accounts')

    class Meta:
        model = Account
        fields = ['item_type']

    def visible_accounts(self, queryset, name, value):
        if value == 'visible':
            return queryset.exclude(item_type__in=['incomebalance', 'spendingbalance'])
        return queryset.filter(*{name: value})
