from django.contrib import admin

from polymorphic.admin import (PolymorphicChildModelAdmin, PolymorphicChildModelFilter,
                               PolymorphicParentModelAdmin)

from apps.counterparties.models import Bank, Counterparty, Person, Shop


@admin.register(Counterparty)
class CounterpartyAdmin(PolymorphicParentModelAdmin):
    base_model = Counterparty
    child_models = [Person, Bank, Shop]
    list_filter = [PolymorphicChildModelFilter]


@admin.register(Person)
class PersonAdmin(PolymorphicChildModelAdmin):
    base_model = Person
    show_in_index = True


@admin.register(Bank)
class BankAdmin(PolymorphicChildModelAdmin):
    base_model = Bank
    show_in_index = True


@admin.register(Shop)
class ShopAdmin(PolymorphicChildModelAdmin):
    base_model = Shop
    show_in_index = True
