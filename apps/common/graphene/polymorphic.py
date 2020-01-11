from graphene_django import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField


class PolyDjangoConnectionFieldMixin:
    def get_manager(self):
        return self.model._default_manager.non_polymorphic()


class PolyDjangoConnectionField(
    PolyDjangoConnectionFieldMixin,
    DjangoConnectionField
):
    pass


class PolyDjangoFilterConnectionField(
    PolyDjangoConnectionFieldMixin,
    DjangoFilterConnectionField
):
    pass


class PolyDjangoObjectTypeMixin:
    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.non_polymorphic()
