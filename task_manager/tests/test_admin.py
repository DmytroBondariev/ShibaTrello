from django.contrib.auth import get_user_model
from django.test import  TestCase
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Test12345!"
        )
        self.client.force_login(user=self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="Test12345!",
            position=self.position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response=response, text=self.worker.position)

    def test_worker_detailed_position_listed(self):
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response=response, text=self.worker.position)
