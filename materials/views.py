from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Payments, Subscription
from materials.paginators import MyPagination
from materials.permissions import IsModerator, IsMaterialsOwner
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from materials.services import stripe_payment_created
from users.models import UserRole


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminUser | ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser | ~IsModerator | IsMaterialsOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAdminUser | IsMaterialsOwner | IsModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAdminUser | IsMaterialsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated | IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == UserRole.MEMBER:
            return Course.objects.filter(owner=self.request.user)
        else:
            return Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        return super().perform_create(serializer)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsAdminUser]
    pagination_class = MyPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsMaterialsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsMaterialsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | ~IsModerator | IsMaterialsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated | IsAdminUser]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def create(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('pk'))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, course=course)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDestroyApiView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated | IsAdminUser]

    def delete(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('pk'))
        subscription = get_object_or_404(Subscription, user=request.user, course=course)
        self.perform_destroy(subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonBuyAPIView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def post(self, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=kwargs.get('pk'))

        lesson_name = lesson.title
        lesson_price = lesson.price
        user = self.request.user.pk

        stripe_session = stripe_payment_created(lesson_name, lesson_price, user)

        return Response({"Payment url": f"{stripe_session.url}"}, status=status.HTTP_200_OK)


class CourseBuyAPIView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def post(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('pk'))

        course_name = course.title
        course_price = course.price
        user = self.request.user.pk

        stripe_session = stripe_payment_created(course_name, course_price, user)

        return Response({"Payment url": f"{stripe_session.url}"}, status=status.HTTP_200_OK)
