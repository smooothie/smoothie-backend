from rest_framework import serializers


class StructureSerializer(serializers.Serializer):
    category_name = serializers.CharField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    currency = serializers.CharField(source='amount_currency', read_only=True)

    def update(self, instance, validated_data):
        return

    def create(self, validated_data):
        return


class DynamicsSerializer(serializers.Serializer):
    period = serializers.DateTimeField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    currency = serializers.CharField(source='amount_currency', read_only=True)
