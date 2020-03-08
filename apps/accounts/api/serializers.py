from django.conf import settings
from django.db.transaction import atomic

from djmoney.money import Money
from rest_framework import serializers

from apps.accounts.models import (Account, CashAccount, CounterpartyAccount, CreditBankAccount,
                                  DebitBankAccount, Deposit, Loan)
from apps.counterparties.models import Counterparty

ACCOUNT_CLASSES = {
    'cashaccount': CashAccount,
    'counterpartyaccount': CounterpartyAccount,
    'debitbankaccount': DebitBankAccount,
    'creditbankaccount': CreditBankAccount,
    'deposit': Deposit,
    'loan': Loan,
}


class SimpleAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):
    item_type = serializers.ChoiceField(choices=[
        ('cashaccount', 'Cash Account'),
        ('counterpartyaccount', 'Counterparty Account'),
        ('debitbankaccount', 'Debit Bank Account'),
        ('creditbankaccount', 'Credit Bank Account'),
        ('deposit', 'Deposit'),
        ('loan', 'Loan'),
    ])
    balance = serializers.FloatField(source='balance.amount', default=0)
    balance_currency = serializers.ChoiceField(choices=settings.CURRENCY_CHOICES,
                                               default=settings.DEFAULT_CURRENCY,
                                               source='balance.currency')
    counterparty_name = serializers.CharField(write_only=True, required=False, default=None,
                                              allow_null=True, allow_blank=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = ['id', 'item_type', 'name', 'balance', 'balance_currency', 'counterparty_name',
                  'user']

    @atomic
    def validate(self, attrs):
        user = self.context['request'].user

        balance = Money(**attrs['balance'])
        attrs['balance'] = balance

        counterparty_name = attrs.pop('counterparty_name', None)
        if attrs['item_type'] == 'counterpartyaccount':
            counterparty_name = counterparty_name or attrs['name']
            counterparty, _ = Counterparty.objects.get_or_create(name=counterparty_name, user=user)
            attrs['counterparty'] = counterparty

        return attrs

    def create(self, validated_data):
        account_cls = ACCOUNT_CLASSES[validated_data.pop('item_type')]
        return account_cls.objects.create(**validated_data)
