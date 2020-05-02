from django.urls import path

from apps.stats.api import views

app_name = 'stats'

urlpatterns = [
    path('structure/', views.structure, name='structure'),
]
