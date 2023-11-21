from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson
from users.models import User


class MemberLessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='member@test.ru',
            password='test',
            role='member',

            is_active=True,
        )
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create(
            email='member2@test.ru',
            password='test',
            role='member',

            is_active=True,
        )

        self.lesson = Lesson.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

        self.lesson2 = Lesson.objects.create(
            title='test2',
            description='test2',
            owner=self.user2
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
        Test for getting list of lessons for member.
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
            {'count': 2, 'next': None, 'previous': None, 'results': [
                {'id': 1, 'title': 'test', 'description': 'test', 'preview': None, 'video_url': None, 'course': None,
                 'owner': 1},
                {'id': 2, 'title': 'test2', 'description': 'test2', 'preview': None, 'video_url': None, 'course': None,
                 'owner': 2}]}
        )

    def test_lesson_create(self):
        """
        Test for creating lesson for member.
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
            3
        )

        self.assertTrue(
            response.json()['owner'] == self.user.pk
        )

    def test_lesson_retrieve(self):
        """
        Test for getting lesson details for member.
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
             'owner': 1}
        )

    def test_invalid_lesson_retrieve(self):
        """
        Test invalid for getting lesson details for member.
        """

        response = self.client.get(
            reverse('materials:lesson-detail', kwargs={'pk': 999}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_another_lesson_retrieve(self):
        """
        Test for getting lesson details another user.
        """
        response = self.client.get(
            reverse('materials:lesson-detail', kwargs={'pk': self.lesson2.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_update(self):
        """
        Test for updating lesson for member.
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
            {'id': 1, 'title': 'test1', 'description': 'test1', 'preview': None, 'video_url': None, 'course': None,
             'owner': 1}
        )

    def test_another_lesson_update(self):
        """
        Test for updating another user lesson for member.
        """

        data = {
            'title': 'test3',
            'description': 'test3'
        }

        response = self.client.put(
            reverse('materials:lesson-update', kwargs={'pk': self.lesson2.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_invalid_lesson_update(self):
        """
        Test invalid for updating lesson  for member.
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
        Test for deleting lesson for member.
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
            1
        )

    def test_another_lesson_delete(self):
        """
        Test for deleting another user lesson for member.
        """

        response = self.client.delete(
            reverse('materials:lesson-delete', kwargs={'pk': self.lesson2.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_invalid_lesson_delete(self):
        """
        Test invalid for deleting lesson  for member.
        """

        response = self.client.delete(
            reverse('materials:lesson-delete', kwargs={'pk': 999})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
