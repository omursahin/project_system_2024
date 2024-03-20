from django.urls import path

from course.views import CourseDetail, CourseCreateList

urlpatterns = [
    path('', CourseCreateList.as_view()),
    path('<int:pk>/', CourseDetail.as_view()),
]
