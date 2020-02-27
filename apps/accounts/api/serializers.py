from rest_framework import serializers

from apps.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(source='balance.amount')

    class Meta:
        model = Account
        fields = ['id', 'item_type', 'name', 'balance', 'balance_currency']
        read_only_fields = fields
