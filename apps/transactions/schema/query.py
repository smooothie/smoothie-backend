from django.db.models import Q

from graphene import relay
from graphene_django import DjangoObjectType

from apps.accounts.models import Account
from apps.common.graphene.polymorphic import (PolyDjangoFilterConnectionField,
                                              PolyDjangoObjectTypeMixin)
from apps.transactions.models import Transaction, TransactionCategory
from ..filters import TransactionFilter


class TransactionCategoryNode(DjangoObjectType):
    class Meta:
        model = TransactionCategory
        fields = ['name']


class TransactionNode(PolyDjangoObjectTypeMixin, DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'amount_currency', 'account_from', 'account_to', 'description',
                  'category', 'is_completed']
        filter_fields = ['category', 'is_completed', 'account_from']
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
        return queryset.filter(
            Q(account_from__user=user) | Q(account_to__user=user)
        ).order_by('-date')


class Query:
    transaction = relay.Node.Field(TransactionNode)
    transactions = PolyDjangoFilterConnectionField(TransactionNode,
                                                   filterset_class=TransactionFilter)
