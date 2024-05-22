from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from semester_course_student.models import SemesterCourseStudent
from semester_course_student.serializers import SemesterCourseStudentSerializer

from semester_course_student.permission import IsAdminAllPermissionAndStudentSafeMethod


# Create your views here.
class SemesterCourseStudentCreateList(generics.ListCreateAPIView):
    serializer_class = SemesterCourseStudentSerializer
    queryset = SemesterCourseStudent.active.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('semester_course__semester__term',
                        'student__first_name', 'student__email')
    search_fields = ('semester_course__semester__term',
                     'student__first_name', 'student__email')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'

class SemesterCourseStudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminAllPermissionAndStudentSafeMethod]
    serializer_class = SemesterCourseStudentSerializer
    queryset = SemesterCourseStudent.active.all()
