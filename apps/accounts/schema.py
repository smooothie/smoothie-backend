from django.core.exceptions import ValidationError
from django.db import transaction

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from apps.accounts.models import Account, CashAccount, CounterpartyAccount
from apps.common.graphene.polymorphic import (PolyDjangoFilterConnectionField,
                                              PolyDjangoObjectTypeMixin)
from apps.counterparties.models import Counterparty
from .filters import AccountFilter

ACCOUNT_CLASSES = {
    'cashaccount': CashAccount,
    'counterpartyaccount': CounterpartyAccount,
}


class AccountNode(PolyDjangoObjectTypeMixin, DjangoObjectType):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance', 'balance_currency', 'transactions_to',
                  'transactions_from']
        filter_fields = ['account_type']
        interfaces = (relay.Node,)

    def resolve_balance(self, info):
        return self.balance.amount

    @classmethod
    def get_queryset(cls, queryset, info):
        queryset = super().get_queryset(queryset, info)
        user = info.context.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=user)


class Query:
    account = relay.Node.Field(AccountNode)
    accounts = PolyDjangoFilterConnectionField(AccountNode, filterset_class=AccountFilter)


class CreateUpdateAccountMutation(relay.ClientIDMutation):
    class Input:
        account_type = graphene.String(required=True)
        name = graphene.String(required=True)
        # TODO: allow providing currency
        balance = graphene.Float()
        counterparty_name = graphene.String()
        id = graphene.ID()

    account = graphene.Field(AccountNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        input['user'] = user

        account_type = input.pop('account_type')
        account_cls = ACCOUNT_CLASSES.get(account_type)
        if account_cls is None:
            account_type_options = ', '.join(ACCOUNT_CLASSES.keys())
            raise ValidationError({
                'accountType': f"accountType must be one of {account_type_options}"
            })

        counterparty_name = input.pop('counterparty_name', None)
        if account_type == 'counterpartyaccount':
            counterparty_name = counterparty_name or input['name']
            counterparty, _ = Counterparty.objects.get_or_create(name=counterparty_name, user=user)
            input['counterparty'] = counterparty

        id_ = input.pop('id', None)

        if id_:
            account = account_cls.objects.get(pk=from_global_id(id_)[1], user=user)
            for k, v in input.items():
                setattr(account, k, v)
        else:
            account = account_cls(**input)

        account.save()

        account = Account.objects.non_polymorphic().get(pk=account.pk)
        return cls(account=account)


class DeleteAccountMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        account = Account.objects.get(pk=from_global_id(id)[1], user=info.context.user)
        account.delete()
        return cls(ok=True)


class AccountMutation:
    account = CreateUpdateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()
