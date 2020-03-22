from djmoney.money import Money
from rest_framework import serializers

from apps.accounts.api.serializers import AccountSerializer
from apps.accounts.models import BankAccount
from apps.common.api.serializer_fields import (CentsField, CurrencyIsoField, DefaultBank,
                                               IntegerDateField, TransactionCategoryNameField)
from apps.common.api.serializers import OtherRepresentationSerializer
from apps.transactions.models import Income, Purchase, Transaction, TransactionCategory
from ..api.serializers import BaseAccountsSerializer, BaseTransactionsSerializer
from .api import MonobankAPI

TRANSACTION_CLASSES = {
    'purchase': Purchase,
    'income': Income,
}


class BaseRetrieveSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)


class AccountsSerializer(BaseRetrieveSerializer, BaseAccountsSerializer):
    bank_api_class = MonobankAPI


class AccountCreateSerializer(OtherRepresentationSerializer, serializers.ModelSerializer):
    representation_serializer_class = AccountSerializer

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


class TransactionCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(write_only=True, source='api_id')
    time = IntegerDateField(write_only=True, source='date')
    description = serializers.CharField(write_only=True)
    mcc = TransactionCategoryNameField(write_only=True, source='category_name')
    amount = CentsField(write_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'time', 'description', 'mcc', 'amount']

    def validate(self, attrs):
        user = self.context['request'].user
        account = BankAccount.objects.get(api_account_id=self.context['account'])
        currency = account.balance_currency
        if attrs['amount'] < 0:
            attrs['item_type'] = 'purchase'
            attrs['amount'] = -attrs['amount']
            attrs['account_from'] = account
            attrs['account_to'] = user.get_spending_balance(currency)
        else:
            attrs['item_type'] = 'income'
            attrs['account_from'] = user.get_income_balance(currency)
            attrs['account_to'] = account
        attrs['amount'] = Money(amount=attrs['amount'], currency=currency)

        category_name = attrs.pop('category_name')
        category = (TransactionCategory.objects.filter(name=category_name).first() or
                    TransactionCategory.objects.create(name=category_name))
        attrs['category'] = category

        return attrs

    def create(self, validated_data):
        item_type = validated_data.pop('item_type')
        try:
            transaction = Transaction.objects.get(api_id=validated_data['api_id'])
        except Transaction.DoesNotExist:
            transaction_cls = TRANSACTION_CLASSES[item_type]
            transaction = transaction_cls(**validated_data)
        else:
            for k, v in validated_data.items():
                setattr(transaction, k, v)
        transaction.save(update_balance=False)
        return transaction


class TransactionsSerializer(BaseRetrieveSerializer, BaseTransactionsSerializer):
    bank_api_class = MonobankAPI
    transaction_create_serializer_class = TransactionCreateSerializer
