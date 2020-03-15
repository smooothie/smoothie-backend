from djmoney.money import Money
from rest_framework import serializers

from apps.accounts.models import BankAccount
from apps.common.api.serializer_fields import CentsField, CurrencyIsoField, DefaultBank
from ..api.serializers import BaseAccountCreateSerializer, BaseAccountsSerializer
from .api import MonobankAPI


class BaseRetrieveSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)


class AccountsSerializer(BaseRetrieveSerializer, BaseAccountsSerializer):
    bank_api_class = MonobankAPI


class AccountCreateSerializer(BaseAccountCreateSerializer):
    id = serializers.CharField(write_only=True, source='api_account_id')
    currency_code = CurrencyIsoField(write_only=True, source='balance.currency')
    balance = CentsField(write_only=True, source='balance.amount')
    bank = serializers.HiddenField(default=DefaultBank(bank_name='Monobank'))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    credit_limit = CentsField(write_only=True)
    masked_pan = serializers.ListField(child=serializers.CharField(), write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = BankAccount
        fields = ['id', 'currency_code', 'balance', 'bank', 'user', 'credit_limit', 'masked_pan',
                  'type']

    def validate(self, attrs):
        # normalize balance
        attrs['balance']['amount'] -= attrs['credit_limit']
        attrs['balance'] = Money(**attrs['balance'])
        attrs['name'] = f"Monobank {attrs.pop('type')} {attrs.pop('masked_pan')[0]}"
        return attrs

    def create(self, validated_data):
        try:
            account = BankAccount.objects.get(api_account_id=validated_data['api_account_id'])
        except BankAccount.DoesNotExist:
            return super().create(validated_data)
        else:
            return super().update(account, validated_data)
