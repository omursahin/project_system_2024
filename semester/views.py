from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from semester.models import Semester
from semester.serializers import SemesterSerializer


# Create your views here.
class SemesterCreateList(generics.ListCreateAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.active.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ('term', 'year')
    search_fields = ('term', 'year')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class SemesterDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.active.all()
    permission_classes = [permissions.IsAdminUser]
