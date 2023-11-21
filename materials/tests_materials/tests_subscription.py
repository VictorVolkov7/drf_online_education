from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Course, Subscription
from users.models import User


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='member@test.ru',
            password='test',
            role='member',
            is_active=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_subscription_create(self):
        """
        Test user subscribe course.
        """

        print(self.course.title)

        response = self.client.post(
            reverse('materials:course-subscribe', kwargs={'pk': self.course.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course)
        )

        response = self.client.get(
            f'/course/{self.course.pk}/',
        )

        self.assertEqual(
            response.json()['is_subscribe'],
            True
        )

    def test_subscription_delete(self):
        """
        Test user unsubscribe course.
        """

        response = self.client.delete(
            reverse('materials:course-unsubscribe', kwargs={'pk': self.course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(
            not Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.get(
            f'/course/{self.course.pk}/',
        )

        print(response.json())

        self.assertEqual(
            response.json()['is_subscribe'],
            False
        )
