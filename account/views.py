# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser

from account.models import MyUser
from account.serializers import UserSerializer
from project_system_2024.core.filter import MyOrderingFilter
from project_system_2024.core.permissions import IsOwner
from project_system_2024.core.renderer import (JSONResponseRenderer,
                                               JSONResponseRendererDetail)


# Create your views here.
class UserCreateList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       MyOrderingFilter]
    filterset_fields = ('email', 'identification_number')
    search_fields = ('email', 'first_name', 'last_name',
                     'identification_number')
    renderer_classes = [JSONResponseRenderer]
    ordering_fields = '__all__'

    # def post(self, request, *args, **kwargs):
    #     password = request.data.get('password')
    #     if not password:
    #         return self.create(request, *args, **kwargs)
    #
    #     request.data['password']
    #     return self.create(request, *args, **kwargs)




class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | IsOwner]
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    renderer_classes = [JSONResponseRendererDetail]
