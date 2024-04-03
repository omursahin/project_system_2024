from django.urls import path


from project_report.views import (ProjectReportCreateList, ProjectReportDetail)

urlpatterns = [
    path('', ProjectReportCreateList.as_view()),
    path('<int:pk>/', ProjectReportDetail.as_view()),
]
