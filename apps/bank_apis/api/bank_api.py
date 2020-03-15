import abc


class BankAPI(abc.ABC):
    @abc.abstractmethod
    def get_accounts(self):
        return []
