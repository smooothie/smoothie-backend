from rest_framework.generics import CreateAPIView
from rest_framework_bulk import BulkCreateAPIView

from apps.accounts.models import Account
from .serializers import AccountCreateSerializer, AccountsSerializer


class ListMonobankAccountsView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountsSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CreateMonobankAccountsView(BulkCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
