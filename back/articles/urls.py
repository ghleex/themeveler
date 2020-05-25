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
    path('theme_notice/<int:theme_pk>/', views.ThemeNoticesView.as_view()),
    path('theme_notice_post/', views.ThemeNoticesPost.as_view()),
    path('theme_notice_change/<int:notice_pk>/', views.ThemeNoticesChange.as_view()),
    path('<int:dest_pk>/comment/', views.Comments.as_view()),
    path('comment_change/<int:comment_pk>/', views.CommentChange.as_view()),
    path('<int:comment_pk>/recomment/', views.ReComments.as_view()),
    path('recomment_change/<int:recomment_pk>/', views.ReCommentChange.as_view()),
    path('<int:comment_pk>/comment/report/', views.ReportCommentMgmt.as_view()),
    path('<int:recomment_pk>/recomment/report/', views.ReportReCommentMgmt.as_view()),
]
