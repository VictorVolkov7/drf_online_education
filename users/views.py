from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)
