from rest_framework import serializers

from apps.accounts.api.serializers import AccountSerializer
from .bank_api import BankAPI


class BankApiSerializer(serializers.Serializer):
    bank_api_class = None

    def _get_api_class(self):
        assert issubclass(self.bank_api_class, BankAPI), (
            f"{self.__class__.__name__} must set `bank_api_class` to a BankAPI subclass"
        )
        return self.bank_api_class

    def create(self, validated_data):
        return self._get_api_class()(**validated_data)

    def update(self, instance, validated_data):
        # TODO
        return


class BaseAccountsSerializer(BankApiSerializer):
    accounts = serializers.SerializerMethodField()

    def get_accounts(self, obj):
        return obj.get_accounts()


class BaseAccountCreateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        super().to_representation(instance)
        return AccountSerializer(instance=instance).to_representation(instance)
