from django.urls import path
from . import views

app_name='articles'
urlpatterns = [
    path('v_category/', views.SetVoiceCategory.as_view()),
    path('v_category/<int:category_pk>/', views.ChangeVoiceCategory.as_view()),
    path('cv/<int:user_pk>/', views.CustomersVoices.as_view()),
    path('cv/<int:user_pk>/<int:voice_pk>/', views.CustomersVoiceChange.as_view()),
    path('cv_reply/<int:manager_pk>/', views.ManagersReplying.as_view()),
    path('cv_reply/<int:manager_pk>/<int:todo_pk>/', views.ManagersReplyChange.as_view()),
    path('theme_notice/<int:theme_pk>/', views.ThemeNoticesView.as_view()),
    path('theme_notice/', views.ThemeNoticesPost.as_view()),
    path('theme_notice/<int:notice_pk>/', views.ThemeNoticesChange.as_view()),
    path('<int:dest_pk>/comment/', views.Comments.as_view()),
    path('comment/<int:comment_pk>/', views.CommentChange.as_view()),
    path('<int:comment_pk>/recomment/', views.ReComments.as_view()),
    path('recomment_change/<int:recomment_pk>/', views.ReCommentChange.as_view()),
    path('report/comment/', views.ReportCommentMgmt.as_view()),
    path('report/recomment/', views.ReportReCommentMgmt.as_view()),
]
