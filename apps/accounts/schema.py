from graphene import relay
from graphene_django import DjangoObjectType

from apps.accounts.models import Account
from apps.common.graphene import PolyDjangoFilterConnectionField, PolyDjangoObjectTypeMixin


class AccountNode(PolyDjangoObjectTypeMixin, DjangoObjectType):
    class Meta:
        model = Account
        filter_fields = {
            'user': ['exact'],
        }
        interfaces = (relay.Node,)


class Query:
    account = relay.Node.Field(AccountNode)
    accounts = PolyDjangoFilterConnectionField(AccountNode)
