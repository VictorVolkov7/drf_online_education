from rest_framework import serializers

from materials.models import Course, Lesson, Payments, Subscription
from materials.validators import UrlsValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlsValidator(field='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(read_only=True, many=True)
    is_subscribe = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, instance):
        return instance.lesson.count()

    def get_is_subscribe(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(course=instance, user=user).exists()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
