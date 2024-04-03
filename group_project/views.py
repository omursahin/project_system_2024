from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from group_project.models import GroupProject
from group_project.serializers import GroupProjectSerializer


# Create your views here.
class GroupProjectCreateList(generics.ListCreateAPIView):
    serializer_class = GroupProjectSerializer
    queryset = GroupProject.active.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('group__id', 'group__title')
    search_fields = ('group__id', 'group__title')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class GroupProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupProjectSerializer
    queryset = GroupProject.active.all()
    permission_classes = [permissions.IsAuthenticated]
