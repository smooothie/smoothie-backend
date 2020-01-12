from graphene import relay
from graphene_django import DjangoObjectType

from apps.accounts.models import Account
from apps.common.graphene.polymorphic import (PolyDjangoFilterConnectionField,
                                              PolyDjangoObjectTypeMixin)
from apps.transactions.models import Transaction, TransactionCategory


class TransactionCategoryNode(DjangoObjectType):
    class Meta:
        model = TransactionCategory
        fields = ['name']


class TranasctionNode(PolyDjangoObjectTypeMixin, DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'amount_currency', 'account_from', 'account_to', 'description',
                  'category', 'is_completed']
        filter_fields = {
            'category': ['exact'],
            'is_completed': ['exact'],
        }
        interfaces = (relay.Node,)

    def resolve_amount(self, info):
        return self.amount.amount

    def resolve_account_from(self, info):
        return Account.objects.non_polymorphic().get(id=self.account_from_id)

    def resolve_account_to(self, info):
        return Account.objects.non_polymorphic().get(id=self.account_to_id)

    @classmethod
    def get_queryset(cls, queryset, info):
        queryset = super().get_queryset(queryset, info)
        user = info.context.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(account_from__user=user)


class Query:
    transaction = relay.Node.Field(TranasctionNode)
    transactions = PolyDjangoFilterConnectionField(TranasctionNode)
