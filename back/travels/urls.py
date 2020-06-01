from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='travels'
urlpatterns = [
    path('', views.map, name='map'),
    path('visited_themes/', views.VisitedThemes.as_view()),
    path('visited_dests/', views.VisitedDest.as_view()),
    path('like/<int:theme_pk>/', views.Like.as_view()),
    path('chat/<int:theme_pk>/', views.Chatting.as_view()),
    path('all_theme/', views.AllTheme.as_view()),
    path('destinations/<int:theme_pk>/', views.Destinations.as_view()),
    path('dest_content/<int:theme_pk>/<int:dest_idx>/', views.DestinationContent.as_view()),
    path('filtered_theme/<region>', views.FilteredTheme.as_view())
]
