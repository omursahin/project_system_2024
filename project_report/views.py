from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from project_report.models import ProjectReport
from project_report.serializers import ProjectReportSerializer


# Create your views here.
class ProjectReportCreateList(generics.ListCreateAPIView):
    serializer_class = ProjectReportSerializer
    queryset = ProjectReport.active.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('project', 'report')













































































































































































    search_fields = ('project', 'report')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class ProjectReportDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectReportSerializer
    queryset = ProjectReport.active.all()
    permission_classes = [permissions.IsAuthenticated]
