import graphene

from apps.accounts.schema import Query as AccountsQuery
from apps.users.schema import Query as UsersQuery


class Query(AccountsQuery, UsersQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
