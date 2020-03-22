from datetime import datetime
from itertools import chain

from django.utils.timezone import make_aware

import pytz
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


class TimestampField(serializers.DateTimeField):
    def to_internal_value(self, data):
        return int(super().to_internal_value(data).timestamp())


class IntegerDateField(serializers.DateTimeField):
    def to_internal_value(self, data):
        return super().to_representation(make_aware(datetime.fromtimestamp(data), pytz.utc))


class TransactionCategoryNameField(serializers.Field):
    def to_internal_value(self, mcc):  # noqa: C901
        if mcc in chain(
                range(3000, 3300),
                range(3351, 3442),
                range(3501, 4000),
                range(4111, 4113),
                range(7032, 7034),
                range(7512, 7514),
                (4011, 4131, 4304, 4411, 4415, 4418, 4457, 4468, 4511, 4582, 4722, 4784, 4789,
                 5962, 7011, 7519,)
        ):
            return 'Подорожі'
        if mcc in (4119, 5047, 5122, 5292, 5295, 5912, 5975, 5976, 5977, 7230, 7297, 7298, 8011,
                   8021, 8031, 8041, 8042, 8043, 8049, 8050, 8062, 8071, 8099):
            return 'Краса та медицина'
        if mcc in chain(
                range(5815, 5819),
                range(5945, 5948),
                range(5970, 5974),
                range(7911, 7923),
                range(7932, 7934),
                range(7991, 7995),
                range(7996, 8000),
                (5733, 5735, 5940, 5941, 7221, 7333, 7395, 7929, 7941, 8664),
        ):
            return 'Розваги та спорт'
        if mcc in range(5811, 5815):
            return 'Кафе та ресторани'
        if mcc in (5297, 5298, 5300, 5311, 5331, 5399, 5411, 5412, 5422, 5441, 5451, 5462, 5499,
                   5715, 5921):
            return 'Продукти й супермаркети'
        if mcc in (7829, 7832, 7841):
            return 'Кіно'
        if mcc in (5172, 5511, 5531, 5532, 5533, 5541, 5542, 5983, 7511, 7523, 7531, 7534, 7535,
                   7538, 7542, 7549):
            return 'Авто та АЗС'
        if mcc in (5131, 5137, 5139, 5611, 5621, 5631, 5641, 5651, 5655, 5661, 5681, 5691, 5697,
                   5698, 5699, 5931, 5948, 5949, 7251, 7296):
            return 'Одяг і взуття'
        if mcc == 4121:
            return 'Таксі'
        if mcc in (742, 5995):
            return 'Тварини'
        if mcc in (2741, 5111, 5192, 5942, 5994):
            return 'Книги'
        if mcc in (5992, 5193):
            return 'Квіти'
        if mcc == 4829:
            return 'Грошові перекази'
        return 'Інше'

    def to_representation(self, name):
        return name


class DefaultBank:
    requires_context = True

    def __init__(self, bank_name):
        self.bank_name = bank_name

    def __call__(self, serializer_field):
        return Bank.objects.get_or_create(user=serializer_field.context['request'].user,
                                          name=self.bank_name)[0]

    def __repr__(self):
        return '%s()' % self.__class__.__name__
