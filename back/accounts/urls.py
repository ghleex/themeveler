from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('signup/', views.SignUp.as_view()),
    path('nickname/<str:nickname>/', views.Nickname.as_view()),
    path('username/<str:username>/', views.Username.as_view()),
    path('email/send/', views.EmailSend.as_view()),
    path('email/auth/<str:username>/<str:confirm_code>/', views.EmailAuth.as_view()),
    path('usermgmt/', views.UserMgmt.as_view()),
    path('password/', views.Password.as_view()),
    path('password/<str:username>/', views.PasswordFind.as_view()),
    path('signin/', views.SignIn.as_view()),
    path('ban/<int:user_pk>/', views.UserBan.as_view()),
    path('social/kakao/', views.KakaoSignInView.as_view()),
    path('social/kakao/callback/', views.KakaoSignInCallbackView.as_view()),
    path('social/google/', views.GoogleSignInView.as_view()),
    path('social/google/callback/', views.GoogleSignInCallbackView.as_view()),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
]