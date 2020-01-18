from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

graphql_view = GraphQLView.as_view(graphiql=settings.DEBUG)
if settings.DEBUG:
    graphql_view = csrf_exempt(graphql_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', graphql_view),
]
