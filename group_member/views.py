from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from group_member.models import GroupMember
from group_member.serializers import GroupMemberSerializer
from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer


# Create your views here.
class GroupMemberCreateList(generics.ListCreateAPIView):
    serializer_class = GroupMemberSerializer
    queryset = GroupMember.active.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('group', 'member')
    search_fields = ('group', 'member')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'


class GroupMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupMemberSerializer
    queryset = GroupMember.active.all()
    permission_classes = [permissions.IsAuthenticated]
