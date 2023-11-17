from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, LimitedUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.kwargs.get('pk') != str(self.request.user.pk):
            return Response({
                'message': 'Нет прав на выполнение этого действия!.',
            }, status=400)

        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list'] and self.kwargs.get('pk') != str(self.request.user.pk):
            return LimitedUserSerializer
        else:
            return UserSerializer
