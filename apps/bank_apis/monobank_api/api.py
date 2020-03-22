from apps.monobank_client import Client
from ..api.bank_api import BankAPI


class MonobankAPI(BankAPI):
    def __init__(self, **kwargs):
        self.client = Client(**kwargs)

    def get_accounts(self):
        client_info = self.client.get_client_info()['data']
        return client_info['accounts']

    def get_transactions(self, from_time, to_time=None, account=None):
        kwargs = {'from_time': from_time, 'to_time': to_time}
        if account is not None:
            kwargs['account'] = account
        return self.client.get_statement(**kwargs)['data']
