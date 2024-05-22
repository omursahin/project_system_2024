from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from course.permissions import IsAdminOrUserCanRead
from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from course.models import Course
from course.serializers import CourseSerializer


# Create your views here.
class CourseCreateList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrUserCanRead]
    queryset = Course.active.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('code', 'title')
    search_fields = ('code', 'title')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrUserCanRead]
    serializer_class = CourseSerializer
    queryset = Course.active.all()
