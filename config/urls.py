from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.accounts.api.views import AccountViewSet
from apps.bank_apis.monobank_api.views import (CreateMonobankAccountsView,
                                               CreateMonobankTransactionsView,
                                               ListMonobankAccountsView)
from apps.counterparties.api.views import CounterpartyAutocompleteViewSet
from apps.stats.api.views import DynamicsViewSet, StructureViewSet
from apps.transactions.api.views import CategoryAutocompleteViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'counterparties/autocomplete', CounterpartyAutocompleteViewSet)
router.register(r'categories/autocomplete', CategoryAutocompleteViewSet)
router.register(r'stats/structure/(?P<account_type>(income|spending))', StructureViewSet)
router.register(r'stats/dynamics/(?P<account_type>(income|spending))', DynamicsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/monobank/accounts/import/', CreateMonobankAccountsView.as_view(),
         name='monobank_accounts_import'),
    path('api/monobank/accounts/', ListMonobankAccountsView.as_view(),
         name='monobank_accounts_list'),
    path('api/monobank/transactions/', CreateMonobankTransactionsView.as_view(),
         name='monobank_transactions'),
    path('api/', include(router.urls))
]
