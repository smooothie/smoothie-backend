import graphene

from apps.accounts.schema import AccountMutation
from apps.accounts.schema import Query as AccountsQuery
from apps.common.schema import TokenMutation
from apps.transactions.schema import Query as TransactionsQuery
from apps.transactions.schema import TransactionMutation
from apps.users.schema import Query as UsersQuery


class Query(
    AccountsQuery,
    TransactionsQuery,
    UsersQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    TokenMutation,
    AccountMutation,
    TransactionMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
