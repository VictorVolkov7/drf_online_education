from users.apps import UsersConfig
from rest_framework import routers

from users.views import UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [

] + router.urls
