from django.urls import path
from . import views

app_name='articles'
urlpatterns = [
    path('set_v_category/', views.SetVoiceCategory.as_view()),
    path('change_v_category/<int:category_pk>/', views.ChangeVoiceCategory.as_view()),
    path('cv/<int:user_pk>/', views.CustomersVoices.as_view()),
    path('cv_change/<int:user_pk>/<int:voice_pk>/', views.CustomersVoiceChange.as_view()),
    path('cv_reply/<int:manager_pk>/', views.ManagersReplying.as_view()),
    path('cv_reply_change/<int:manager_pk>/<int:todo_pk>/', views.ManagersReplyChange.as_view()),
    path('report/comment/', views.ReportCommentMgmt.as_view()),
    path('report/recomment/', views.ReportReCommentMgmt.as_view()),
]
