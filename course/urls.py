from django.urls import path

from semester.views import SemesterCreateList, SemesterDetail

urlpatterns = [
    path('', SemesterCreateList.as_view()),
    path('<int:pk>/', SemesterDetail.as_view()),
]
