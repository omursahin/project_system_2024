from django.urls import path

from academician_group_grade.views import (AcademicianGroupGradeCreateList,
                                           AcademicianGroupGradeDetail)

urlpatterns = [
    path('', AcademicianGroupGradeCreateList.as_view()),
    path('<int:pk>/', AcademicianGroupGradeDetail.as_view()),
]
