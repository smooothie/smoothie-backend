from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from apps.accounts.api.views import AccountViewSet
from apps.transactions.api.views import TransactionViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)


graphql_view = GraphQLView.as_view(graphiql=settings.DEBUG)
if settings.DEBUG:
    graphql_view = csrf_exempt(graphql_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', graphql_view),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
