from django.contrib.auth.decorators import permission_required
from django.urls import path
from . import views

app_name='articles'
urlpatterns = [
    path('set_v_category/', permission_required('is_staff')(views.SetVoiceCategory.as_view())),
    path('change_v_category/<int:category_pk>/', permission_required('is_staff')(views.ChangeVoiceCategory.as_view())),
    path('cv/<int:user_pk>/', views.CustomersVoices.as_view()),
    path('cv_change/<int:user_pk>/<int:voice_pk>/', views.CustomersVoiceChange.as_view()),
    path('cv_reply/<int:manager_pk>/', permission_required('is_staff')(views.ManagersReplying.as_view())),
    path('cv_reply_change/<int:manager_pk>/<int:todo_pk>/', permission_required('is_staff')(views.ManagersReplyChange.as_view())),
]
