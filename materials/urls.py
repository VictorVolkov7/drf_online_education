from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework import routers

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyApiView

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # payments
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),

    # subscription
    path('course/<int:pk>/subscribe/', SubscriptionCreateAPIView.as_view(), name='course-subscribe'),
    path('course/<int:pk>/unsubscribe/', SubscriptionDestroyApiView.as_view(), name='course-unsubscribe')
] + router.urls
