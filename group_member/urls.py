from django.urls import path

from group_member.views import GroupMemberDetail, GroupMemberCreateList

urlpatterns = [
    path('', GroupMemberCreateList.as_view()),
    path('<int:pk>/', GroupMemberDetail.as_view()),
]
