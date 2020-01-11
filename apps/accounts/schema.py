from graphene import relay
from graphene_django import DjangoObjectType

from apps.accounts.models import Account
from apps.common.graphene.polymorphic import (PolyDjangoFilterConnectionField,
                                              PolyDjangoObjectTypeMixin)


class AccountNode(PolyDjangoObjectTypeMixin, DjangoObjectType):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance', 'balance_currency']
        filter_fields = {
            'account_type': ['exact'],
        }
        interfaces = (relay.Node,)

    def resolve_balance(self, info):
        return self.balance.amount

    @classmethod
    def get_queryset(cls, queryset, info):
        queryset = super().get_queryset(queryset, info)
        user = info.context.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=user).exclude(
            account_type__in=['incomebalance', 'spendingbalance'])


class Query:
    account = relay.Node.Field(AccountNode)
    accounts = PolyDjangoFilterConnectionField(AccountNode)
