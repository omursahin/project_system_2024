from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions

from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.renderer import JSONResponseRenderer
from group.models import Group
from group.serializers import GroupSerializer


# Create your views here.
class GroupCreateList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.active.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('owner__first_name', 'owner__last_name',
                        'title')
    search_fields = ('owner__first_name', 'owner__last_name', 'title')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'



class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.active.all()
    permission_classes = [permissions.IsAuthenticated]