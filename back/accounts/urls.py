from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('user/', views.UserMgmt.as_view()),
    path('nickname/', views.Nickname.as_view()),
    path('username/', views.Username.as_view()),
    path('mail/', views.Mail.as_view()),
]