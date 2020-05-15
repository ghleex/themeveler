from django.urls import path
from . import views
app_name='travels'
urlpatterns = [
    path('', views.map, name='map'),
    path('mgmt/<int:pk>/', views.TravelMgmt.as_view()),
    path('chat/', views.Chating.as_view()),
]
