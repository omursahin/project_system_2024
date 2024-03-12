from django.urls import path

from account.views import UserCreateList, UserDetail

urlpatterns = [
    path('', UserCreateList.as_view()),
    path('<int:pk>/', UserDetail.as_view()),
]
