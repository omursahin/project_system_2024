from django.urls import path

from semester_course_student.views import (SemesterCourseStudentCreateList,
                                           SemesterCourseStudentDetail)

urlpatterns = [
    path('', SemesterCourseStudentCreateList.as_view()),
    path('<int:pk>/', SemesterCourseStudentDetail.as_view()),
]
