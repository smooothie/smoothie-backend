import abc


class BankAPI(abc.ABC):
    @abc.abstractmethod
    def get_accounts(self):
        return []

    @abc.abstractmethod
    def get_transactions(self, from_time, to_time=None, account=None):
        return []
