from django.urls import path

from group_project.views import (GroupProjectCreateList, GroupProjectDetail)

urlpatterns = [
    path('', GroupProjectCreateList.as_view()),
    path('<int:pk>/', GroupProjectDetail.as_view()),
]
