from django.conf import settings
from django.db.transaction import atomic

from djmoney.money import Money
from rest_framework import serializers

from apps.accounts.models import (Account, BankAccount, CashAccount, CounterpartyAccount, Deposit,
                                  Loan)
from apps.counterparties.models import Bank, Counterparty

ACCOUNT_CLASSES = {
    'cashaccount': CashAccount,
    'counterpartyaccount': CounterpartyAccount,
    'bankaccount': BankAccount,
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
        ('bankaccount', 'Bank Account'),
        ('deposit', 'Deposit'),
        ('loan', 'Loan'),
    ])
    balance = serializers.FloatField(source='balance.amount', default=0)
    balance_currency = serializers.ChoiceField(choices=settings.CURRENCY_CHOICES,
                                               default=settings.DEFAULT_CURRENCY,
                                               source='balance.currency')
    counterparty_name = serializers.CharField(write_only=True, required=False, default=None,
                                              allow_null=True, allow_blank=True)
    bank_name = serializers.CharField(write_only=True, required=False, default=None,
                                      allow_null=True, allow_blank=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    credit_limit = serializers.FloatField()
    api_account_id = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'item_type', 'name', 'balance', 'balance_currency', 'counterparty_name',
                  'bank_name', 'user', 'credit_limit', 'api_account_id']

    def get_api_account_id(self, obj):
        return getattr(obj, 'api_account_id', None)

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

        bank_name = attrs.pop('bank_name', None)
        if attrs['item_type'] in ['bankaccount', 'deposit', 'loan']:
            if not bank_name:
                raise serializers.ValidationError({
                    'bank_name': "Це поле обов'язкове",
                })
            bank, _ = Bank.objects.get_or_create(name=bank_name, user=user)
            attrs['bank'] = bank

        return attrs

    def create(self, validated_data):
        account_cls = ACCOUNT_CLASSES[validated_data.pop('item_type')]
        return account_cls.objects.create(**validated_data)
