from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('user/', views.SignUp.as_view()),
    path('nickname/', views.Nickname.as_view()),
    path('username/', views.Username.as_view()),
    path('mail/', views.Mail.as_view()),
    path('usermgmt/', views.UserMgmt.as_view()),
    path('password/', views.Password.as_view()),
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
]