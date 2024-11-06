from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from good_habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", tg_username="@Ankhatin")
        self.habit = Habit.objects.create(
            action="Выпить стакан молока",
            first_date=timezone.now().date(),
            time_of_action=timezone.now().time(),
            time_to_perform=120,
            frequency=1,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_list(self):
        url = reverse("users:user_habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_user(self):
        url = reverse("users:user_create")
        self.data = {
            "email": "test@test.com",
            "password": "test",
            "tg_username": "test",
        }
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
