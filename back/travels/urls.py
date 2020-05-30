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
    path('start/<int:theme_pk>/', views.TravelTheme.as_view()),
    path('all_theme/', views.AllTheme.as_view()),
    path('selected_theme/<region>', views.SelectedTheme.as_view())
]
