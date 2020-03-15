from moneyed import get_currency
from rest_framework import serializers

from apps.counterparties.models import Bank


class CurrencyIsoField(serializers.Field):
    def to_internal_value(self, data):
        return get_currency(iso=data)

    def to_representation(self, value):
        return None


class CentsField(serializers.IntegerField):
    def to_internal_value(self, data):
        return super().to_internal_value(data) / 100

    def to_representation(self, value):
        return super().to_representation(value * 100)


class DefaultBank:
    requires_context = True

    def __init__(self, bank_name):
        self.bank_name = bank_name

    def __call__(self, serializer_field):
        return Bank.objects.get_or_create(user=serializer_field.context['request'].user,
                                          name=self.bank_name)[0]

    def __repr__(self):
        return '%s()' % self.__class__.__name__
