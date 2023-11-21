from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson
from users.models import User


class SULessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='admin@test.ru',
            password='test',

            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title='test',
            description='test',
        )

    def tearDown(self):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        super().tearDown()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT setval(pg_get_serial_sequence('"users_user"','id'), 1, false);
                SELECT setval(pg_get_serial_sequence('"materials_lesson"','id'), 1, false);
            """)

    def test_get_list(self):
        """
        Test for getting list of lessons for admin.
        """

        response = self.client.get(
            reverse('materials:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 1, 'title': 'test', 'description': 'test', 'preview': None, 'video_url': None, 'course': None,
                 'owner': None}]}
        )

    def test_lesson_create(self):
        """
        Test for creating lesson for admin.
        """
        data = {
            'title': 'test1',
            'description': 'test1',
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

        self.assertTrue(
            response.json()['owner'] == self.user.pk
        )

    def test_lesson_create_validation_error(self):
        """
        Test(validation error) for creating lesson for admin.
        """
        data = {
            'title': 'test3',
            'description': 'test3',
            'video_url': 'https://rutube.ru/video/c6cc4d620b1d4338901770a44b3e82f4/'
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Видео может быть только с YouTube']}
        )

    def test_lesson_retrieve(self):
        """
        Test for getting lesson details  for admin.
        """

        response = self.client.get(
            reverse('materials:lesson-detail', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk, 'title': 'test', 'description': 'test', 'preview': None, 'video_url': None,
             'course': None,
             'owner': None}
        )

    def test_invalid_lesson_retrieve(self):
        """
        Test invalid for getting lesson details  for admin.
        """

        response = self.client.get(
            reverse('materials:lesson-detail', kwargs={'pk': 999}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_lesson_update(self):
        """
        Test for updating lesson  for admin.
        """

        data = {
            'title': 'test1',
            'description': 'test1'
        }

        response = self.client.put(
            reverse('materials:lesson-update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk, 'title': 'test1', 'description': 'test1', 'preview': None, 'video_url': None,
             'course': None, 'owner': None}
        )

    def test_invalid_lesson_update(self):
        """
        Test invalid for updating lesson  for admin.
        """

        data = {
            'title': 'test999',
            'description': 'test999'
        }

        response = self.client.put(
            reverse('materials:lesson-update', kwargs={'pk': 999}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_lesson_delete(self):
        """
        Test for deleting lesson  for admin.
        """

        response = self.client.delete(
            reverse('materials:lesson-delete', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )

    def test_invalid_lesson_delete(self):
        """
        Test invalid for deleting lesson  for admin.
        """

        response = self.client.delete(
            reverse('materials:lesson-delete', kwargs={'pk': 999})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
