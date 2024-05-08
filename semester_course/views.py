from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.permissions import IsOwner, IsAdminOrReadOnly
from project_system_2024.core.renderer import JSONResponseRenderer
from semester_course.models import SemesterCourse
from semester_course.serializers import SemesterCourseSerializer


# Create your views here.
class SemesterCourseCreateList(generics.ListCreateAPIView):
    serializer_class = SemesterCourseSerializer
    queryset = SemesterCourse.active.all()
    permission_classes = [permissions.IsAdminUser | IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('semester__term', 'semester__year',
                        'course__code', 'course__title')
    search_fields = ('semester__term', 'semester__year',
                     'course__code', 'course__title')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class SemesterCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SemesterCourseSerializer
    queryset = SemesterCourse.active.all()
    permission_classes = [permissions.IsAuthenticated]

