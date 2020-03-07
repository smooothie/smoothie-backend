import django_filters as filters

from apps.accounts.models import Account


class AccountFilter(filters.FilterSet):
    exclude_id = filters.NumberFilter(field_name='id', exclude=True)

    class Meta:
        model = Account
        fields = ['item_type', 'exclude_id']
