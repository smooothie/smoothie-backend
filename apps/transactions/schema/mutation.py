from django.core.exceptions import ValidationError
from django.db.transaction import atomic

import graphene
from graphene import relay
from graphql_relay import from_global_id

from apps.accounts.models import Account
from apps.counterparties.models import Counterparty
from apps.transactions.models import Income, Purchase, Transaction, TransactionCategory, Transfer
from .query import TransactionNode

TRANSACTION_CLASSES = {
    'purchase': Purchase,
    'income': Income,
    'transfer': Transfer,
}


class CreateTransactionMutation(relay.ClientIDMutation):
    class Input:
        item_type = graphene.String(required=True)
        # TODO: allow providing currency
        amount = graphene.Float(required=True)
        date = graphene.DateTime()
        account_from_id = graphene.ID()
        account_to_id = graphene.ID()
        description = graphene.String()
        category = graphene.String(required=True)
        is_completed = graphene.Boolean()
        counterparty_name = graphene.String()

    transaction = graphene.Field(TransactionNode)

    @classmethod
    @atomic
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        item_type = input.pop('item_type')
        transaction_cls = TRANSACTION_CLASSES.get(item_type)
        if transaction_cls is None:
            item_type_options = ', '.join(TRANSACTION_CLASSES.keys())
            raise ValidationError({
                'itemType': f"itemType must be one of {item_type_options}"
            })

        account_to_id = input.pop('account_to_id', None)
        if item_type == 'purchase':
            account_to = user.spending_balance
        else:
            if not account_to_id:
                raise ValidationError({
                    'account_to_id': 'This field is required',
                })
            account_to = Account.objects.get(pk=from_global_id(account_to_id)[1], user=user)
        input['account_to'] = account_to

        account_from_id = input.pop('account_from_id', None)
        if item_type == 'income':
            account_from = user.income_balance
        else:
            if not account_from_id:
                raise ValidationError({
                    'account_from_id': 'This field is required',
                })
            account_from = Account.objects.get(pk=from_global_id(account_from_id)[1], user=user)
        input['account_from'] = account_from

        category_name = input.pop('category')
        input['category'] = TransactionCategory.objects.get_or_create(name=category_name)[0]

        counterparty_name = input.pop('counterparty_name', None)
        if item_type in ['purchase', 'income']:
            if not counterparty_name:
                raise ValidationError({
                    'counterparty_name': 'This field is required',
                })
            counterparty, _ = Counterparty.objects.get_or_create(name=counterparty_name, user=user)
            input['counterparty'] = counterparty

        transaction = transaction_cls.objects.create(**input)
        transaction = Transaction.objects.non_polymorphic().get(pk=transaction.pk)

        return cls(transaction=transaction)


class DeleteTransactionMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        transaction = Transaction.objects.get(pk=from_global_id(id)[1], user=info.context.user)
        transaction.delete()
        return cls(ok=True)


class TransactionMutation:
    transaction = CreateTransactionMutation.Field()
    delete_transaction = DeleteTransactionMutation.Field()
