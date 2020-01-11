from django.conf import settings
from django.contrib import admin
from django.urls import path

from apps.common.graphene.views import PrivateGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', PrivateGraphQLView.as_view(graphiql=settings.DEBUG)),
]
