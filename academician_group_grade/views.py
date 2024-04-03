from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from academician_group_grade.models import AcademicianGroupGrade
from academician_group_grade.serializers import AcademicianGroupGradeSerializer


# Create your views here.
class AcademicianGroupGradeCreateList(generics.ListCreateAPIView):
    serializer_class = AcademicianGroupGradeSerializer
    queryset = AcademicianGroupGrade.active.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('academician__first_name',
                        'academician__last_name', 'academician__email')
    search_fields = ('academician__first_name',
                     'academician__last_name', 'academician__email')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class AcademicianGroupGradeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AcademicianGroupGradeSerializer
    queryset = AcademicianGroupGrade.active.all()
    permission_classes = [permissions.IsAdminUser]
