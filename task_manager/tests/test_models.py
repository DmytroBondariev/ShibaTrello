from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from task_manager.models import Position, TaskType, Task


class PositionModelTests(TestCase):
    def test_position_str(self):
        test_position = Position.objects.create(name="Developer")
        self.assertEqual(
            str(test_position),
            test_position.name
        )


class TaskTypeModelTests(TestCase):
    def test_task_type_str(self):
        test_task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(
            str(test_task_type),
            test_task_type.name
        )


class TaskModelTests(TestCase):

    def test_task_str(self):
        test_task_type = TaskType.objects.create(name='Bug')
        test_task = Task.objects.create(
            name='Task Testing',
            description='Lorem ipsum dolor sit amet',
            deadline=timezone.now() + timezone.timedelta(minutes=11),
            priority='High',
            task_type=test_task_type
        )

        self.assertEqual(
            str(test_task),
            f"Task number: {test_task.id}. Topic: {test_task.name}"
        )

    def test_invalid_task_deadline(self):
        test_task_type = TaskType.objects.create(name='Bug')
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name='Task Testing',
                description='Lorem ipsum dolor sit amet',
                deadline=timezone.now() - timezone.timedelta(minutes=10),
                priority='High',
                task_type=test_task_type
            )

    def test_invalid_task_min_deadline(self):
        test_task_type = TaskType.objects.create(name='Bug')
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name='Task 4',
                description='Lorem ipsum dolor sit amet',
                deadline=timezone.now() + timezone.timedelta(minutes=5),
                priority='High',
                task_type=test_task_type
            )


class WorkerModelTests(TestCase):
    def test_worker_str(self):
        test_position = Position.objects.create(name='Developer')
        test_worker = get_user_model().objects.create(
            username='test_user',
            first_name="Test name",
            last_name="Test Last name",
            position=test_position
        )
        self.assertEqual(
            str(test_worker),
            f"{test_worker.username} "
            f"({test_worker.first_name} {test_worker.last_name}, "
            f"position: {test_worker.position})"
        )
