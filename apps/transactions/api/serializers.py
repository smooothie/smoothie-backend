from rest_framework import serializers

from apps.transactions.models import Transaction, TransactionCategory


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['name']
        read_only_fields = fields


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(source='amount.amount')
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'amount', 'amount_currency', 'account_from', 'account_to',
                  'description', 'category', 'is_completed']
        read_only_fields = fields
