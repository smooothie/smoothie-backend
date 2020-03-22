from collections.abc import Iterable

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class OtherRepresentationSerializer:
    representation_serializer_class = None

    @property
    def data(self):
        # call grandparent's property
        ret = super(serializers.Serializer, self).data
        if isinstance(ret, dict):
            return ReturnDict(ret, serializer=self)
        if isinstance(ret, list):
            return ReturnList(ret, serializer=self)
        return ret

    def to_representation(self, instance):
        assert issubclass(self.representation_serializer_class, serializers.Serializer)
        many = isinstance(instance, Iterable)
        serializer = self.representation_serializer_class(instance, many=many)
        return serializer.data
