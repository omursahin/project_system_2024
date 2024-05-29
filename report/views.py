from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from report.models import Report
from report.permission import IsAuthenticatedForCreate
from report.serializers import ReportSerializer


# Create your views here.
class ReportCreateList(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.active.all()
    permission_classes = [permissions.IsAdminUser | IsAuthenticatedForCreate]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('semester_course__semester__term',
                        'semester_course__semester__year', 'title')
    search_fields = ('semester_course__semester__term',
                     'semester_course__semester__year', 'title')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.active.all()
    permission_classes = [permissions.IsAdminUser]
