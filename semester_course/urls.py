from django.urls import path


from semester_course.views import (SemesterCourseCreateList,
                                   SemesterCourseDetail)

urlpatterns = [
    path('', SemesterCourseCreateList.as_view()),
    path('<int:pk>/', SemesterCourseDetail.as_view(),name='your-model-detail'),
]
