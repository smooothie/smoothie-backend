from rest_framework import serializers

from apps.counterparties.models import Counterparty


class SimpleCounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = ['id', 'name']
        read_only_fields = fields
