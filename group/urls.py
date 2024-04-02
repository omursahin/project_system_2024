from django.urls import path


from group.views import (GroupCreateList, GroupDetail)

urlpatterns = [
    path('', GroupCreateList.as_view()),
    path('<int:pk>/', GroupDetail.as_view()),
]
