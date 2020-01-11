from graphene import relay
from graphene_django import DjangoConnectionField, DjangoObjectType

from apps.users.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)


class Query:
    user = relay.Node.Field(UserNode)
    users = DjangoConnectionField(UserNode)
