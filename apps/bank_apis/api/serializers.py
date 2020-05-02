from django.utils import timezone

from djangorestframework_camel_case.util import underscoreize
from rest_framework import serializers

from apps.common.api.serializer_fields import TimestampField
from apps.common.api.serializers import OtherRepresentationSerializer
from apps.transactions.api.serializers import TransactionSerializer
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


class BaseTransactionsSerializer(OtherRepresentationSerializer, BankApiSerializer):
    transaction_create_serializer_class = None
    representation_serializer_class = TransactionSerializer
    max_time_interval = None

    from_time = TimestampField(write_only=True)
    to_time = TimestampField(write_only=True, default=timezone.now)
    account = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if (self.max_time_interval and
                attrs['to_time'] - attrs['from_time'] > self.max_time_interval):
            interval = timezone.timedelta(seconds=self.max_time_interval)
            raise serializers.ValidationError(
                f'Максимальний часовий інтервал становить {interval.days} днів'
            )
        return attrs

    def create(self, validated_data):
        assert issubclass(self.transaction_create_serializer_class, serializers.Serializer)
        data_copy = validated_data.copy()
        from_time = data_copy.pop('from_time')
        to_time = data_copy.pop('to_time', None)
        account = data_copy.pop('account')
        bank_api = super().create(data_copy)
        raw_transactions = bank_api.get_transactions(from_time, to_time, account)
        create_serializer = self.transaction_create_serializer_class(
            data=list(map(underscoreize, raw_transactions)),
            many=True,
            context={
                'request': self.context['request'],
                'account': self.validated_data['account'],
            }
        )
        create_serializer.is_valid(raise_exception=True)
        instances = create_serializer.save()
        return instances

    def update(self, instance, validated_data):
        # TODO
        return
