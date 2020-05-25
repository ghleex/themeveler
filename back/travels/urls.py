from django.urls import path
from . import views

app_name='travels'
urlpatterns = [
    path('', views.map, name='map'),
    path('visited_themes/', views.VisitedThemes.as_view()),
    path('visited_dests/', views.VisitedDest.as_view()),
    path('like/<int:theme_pk>/', views.Like.as_view()),
    path('chat/<int:theme_pk>/', views.Chatting.as_view()),
]
