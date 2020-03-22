from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.transaction import atomic

from djmoney.money import Money
from rest_framework import serializers

from apps.accounts.models import Account
from apps.counterparties.models import Counterparty
from apps.transactions.models import Income, Purchase, Transaction, TransactionCategory, Transfer

TRANSACTION_CLASSES = {
    'purchase': Purchase,
    'income': Income,
    'transfer': Transfer,
}


class SimpleAccountSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(source='balance.amount', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance']
        read_only_fields = fields


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['name']
        read_only_fields = fields


class TransactionSerializer(serializers.ModelSerializer):
    item_type = serializers.ChoiceField(choices=[
        ('income', 'income'),
        ('purchase', 'purchase'),
        ('transfer', 'transfer'),
    ])
    amount = serializers.FloatField(source='amount.amount')
    amount_currency = serializers.CharField(source='amount.currency', read_only=True)
    account_from = SimpleAccountSerializer(read_only=True)
    account_to = SimpleAccountSerializer(read_only=True)
    account_from_id = serializers.PrimaryKeyRelatedField(
        source='account_from', write_only=True, required=False, default=None,
        allow_null=True,
        queryset=Account.objects.visible())
    account_to_id = serializers.PrimaryKeyRelatedField(
        source='account_to', write_only=True, required=False, default=None,
        allow_null=True,
        queryset=Account.objects.visible())
    category = TransactionCategorySerializer(read_only=True)
    category_name = serializers.CharField(write_only=True, required=True)
    counterparty_name = serializers.CharField(write_only=True, required=False, default=None,
                                              allow_null=True, allow_blank=True)
    is_completed = serializers.BooleanField(default=True)

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'amount', 'amount_currency', 'account_from', 'account_to',
                  'account_from_id', 'account_to_id', 'description', 'category', 'is_completed',
                  'counterparty_name', 'item_type', 'category_name']

    def _validate_accounts(self, attrs):
        user = self.context['request'].user

        if attrs['item_type'] == 'purchase':
            required_accounts = ['account_from']
        elif attrs['item_type'] == 'income':
            required_accounts = ['account_to']
        else:
            required_accounts = ['account_from', 'account_to']

        for required_account in required_accounts:
            if not attrs.get(required_account):
                raise serializers.ValidationError({
                    f'{required_account}_id': "Це поле обов'язкове",
                })

        if attrs['item_type'] == 'purchase':
            currency = attrs['account_from'].balance_currency
            attrs['account_to'] = user.get_spending_balance(currency)
        elif attrs['item_type'] == 'income':
            currency = attrs['account_to'].balance_currency
            attrs['account_from'] = user.get_income_balance(currency)
        else:
            currency = attrs['account_from'].balance_currency
            if currency != attrs['account_to'].balance_currency:
                raise serializers.ValidationError(
                    'Валюта операції повинна співпадати з валютою обох рахунків')

        amount = Money(amount=attrs['amount']['amount'], currency=currency)
        attrs['amount'] = amount

    def _validate_balance(self, attrs):
        current_balance = attrs['account_from'].balance
        try:
            attrs['account_from'].balance = current_balance - attrs['amount']
            attrs['account_from'].clean()
        except DjangoValidationError:
            raise serializers.ValidationError({
                'amount': "Переконайтеся, що на рахунку достатньо коштів",
            })
        finally:
            attrs['account_from'].balance = current_balance

    def _validate_counterparty(self, attrs):
        user = self.context['request'].user

        counterparty_name = attrs.pop('counterparty_name', None)
        if attrs['item_type'] in ['purchase', 'income']:
            if not counterparty_name:
                raise serializers.ValidationError({
                    'counterparty_name': "Це поле обов'язкове",
                })
            counterparty, _ = Counterparty.objects.get_or_create(name=counterparty_name, user=user)
            attrs['counterparty'] = counterparty

    def _validate_category(self, attrs):
        category_name = attrs.pop('category_name')
        category = (TransactionCategory.objects.filter(name=category_name).first() or
                    TransactionCategory.objects.create(name=category_name))
        attrs['category'] = category

    @atomic
    def validate(self, attrs):
        self._validate_accounts(attrs)
        self._validate_balance(attrs)
        self._validate_counterparty(attrs)
        self._validate_category(attrs)
        return attrs

    def create(self, validated_data):
        transaction_cls = TRANSACTION_CLASSES[validated_data.pop('item_type')]
        return transaction_cls.objects.create(**validated_data)
