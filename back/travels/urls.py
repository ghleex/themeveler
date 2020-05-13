from django.urls import path
from . import views
app_name='travels'
urlpatterns = [
    path('', views.map, name='map')
]
