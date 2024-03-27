from django.urls import path

from report.views import ReportCreateList, ReportDetail

urlpatterns = [
    path('', ReportCreateList.as_view()),
    path('<int:pk>/', ReportDetail.as_view()),
]
