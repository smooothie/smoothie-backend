from apps.monobank_client import Client
from ..api.bank_api import BankAPI


class MonobankAPI(BankAPI):
    def __init__(self, **kwargs):
        self.client = Client(**kwargs)

    def get_accounts(self):
        client_info = self.client.get_client_info()['data']
        return client_info['accounts']
