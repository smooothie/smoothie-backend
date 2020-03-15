from django.contrib import admin

from polymorphic.admin import (PolymorphicChildModelAdmin, PolymorphicChildModelFilter,
                               PolymorphicParentModelAdmin)

from apps.accounts.models import (Account, BankAccount, CashAccount, CounterpartyAccount, Deposit,
                                  IncomeBalance, Loan, SpendingBalance)


@admin.register(Account)
class AccountAdmin(PolymorphicParentModelAdmin):
    base_model = Account
    child_models = [CashAccount, CounterpartyAccount, BankAccount,
                    Deposit, Loan, IncomeBalance, SpendingBalance]
    list_filter = [PolymorphicChildModelFilter]


@admin.register(CashAccount)
class CashAccountAdmin(PolymorphicChildModelAdmin):
    base_model = CashAccount
    show_in_index = True


@admin.register(IncomeBalance)
class IncomeBalanceAdmin(PolymorphicChildModelAdmin):
    base_model = IncomeBalance
    show_in_index = True


@admin.register(SpendingBalance)
class SpendingBalanceAdmin(PolymorphicChildModelAdmin):
    base_model = SpendingBalance
    show_in_index = True


@admin.register(CounterpartyAccount)
class CounterpartyAccountAdmin(PolymorphicChildModelAdmin):
    base_model = CounterpartyAccount
    show_in_index = True


@admin.register(BankAccount)
class BankAccountAdmin(PolymorphicChildModelAdmin):
    base_model = BankAccount
    show_in_index = True


@admin.register(Deposit)
class DepositAdmin(PolymorphicChildModelAdmin):
    base_model = Deposit
    show_in_index = True


@admin.register(Loan)
class LoanAdmin(PolymorphicChildModelAdmin):
    base_model = Loan
    show_in_index = True
