from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Position, TaskType, Task

TASKS_URL = reverse("task_manager:task-list")


class PublicTaskTests(TestCase):

    def test_login_required(self):
        response = self.client.get(TASKS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.user = get_user_model().objects.create_user(
            username="test_worker",
            password="Test12345!",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_tasks(self):
        Task.objects.create(
            name='Task Testing',
            description='Lorem ipsum dolor sit amet',
            deadline=timezone.now() + timezone.timedelta(minutes=11),
            priority='High',
            task_type=self.task_type
        )

        Task.objects.create(
            name='Task Testing Two',
            description='Lorem ipsum dolor sit amet',
            deadline=timezone.now() + timezone.timedelta(minutes=11),
            priority='High',
            task_type=self.task_type
        )

        response = self.client.get(TASKS_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertTemplateUsed(
            response=response,
            template_name="pages/task_list.html"
        )


class ToggleAssignToTaskViewTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword12345'
        )
        self.task = Task.objects.create(
            name='Task Testing',
            description='Lorem ipsum dolor sit amet',
            deadline=timezone.now() + timezone.timedelta(minutes=11),
            priority='High',
            task_type=self.task_type
        )

    def test_toggle_assign_to_task(self):
        self.client.login(
            username='testuser',
            password='testpassword12345'
        )

        response = self.client.get(
            reverse(
                'task_manager:toggle-task-assign', args=[self.task.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.worker.tasks.filter(pk=self.task.id).exists())

        response = self.client.get(
            reverse(
                'task_manager:toggle-task-assign', args=[self.task.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.worker.tasks.filter(pk=self.task.id).exists())


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        Position.objects.create(name="CEO")
        Position.objects.create(name="Project Manager")
        TaskType.objects.create(name="Bug")
        TaskType.objects.create(name="New feature")

    def test_index_view(self):
        response = self.client.get(reverse('task_manager:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["num_positions"] == 2)
        self.assertTrue(response.context["num_task_types"] == 2)
