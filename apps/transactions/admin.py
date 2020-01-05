from django.contrib import admin

from polymorphic.admin import (PolymorphicChildModelAdmin, PolymorphicChildModelFilter,
                               PolymorphicParentModelAdmin)

from apps.transactions.models import Income, Purchase, Transaction, TransactionCategory, Transfer


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(Transaction)
class TransactionAdmin(PolymorphicParentModelAdmin):
    base_model = Transaction
    child_models = [Purchase, Income, Transfer]
    list_filter = [PolymorphicChildModelFilter]
    list_display = ['date', 'amount', 'description', 'category', 'is_completed']


@admin.register(Purchase)
class PurchaseAdmin(PolymorphicChildModelAdmin):
    base_model = Purchase
    show_in_index = True


@admin.register(Income)
class IncomeAdmin(PolymorphicChildModelAdmin):
    base_model = Income
    show_in_index = True


@admin.register(Transfer)
class TransferAdmin(PolymorphicChildModelAdmin):
    base_model = Transfer
    show_in_index = True
