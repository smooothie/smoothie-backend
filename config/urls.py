from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.accounts.api.views import AccountViewSet
from apps.counterparties.api.views import CounterpartyAutocompleteViewSet
from apps.transactions.api.views import CategoryAutocompleteViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'counterparties/autocomplete', CounterpartyAutocompleteViewSet)
router.register(r'categories/autocomplete', CategoryAutocompleteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls))
]
