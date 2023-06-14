from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from task_manager.models import Position, TaskType, Task, Worker


class TaskModelTestCase(TestCase):
    def test_valid_task(self):
        test_task_type = TaskType.objects.create(name='Bug')
        task = Task.objects.create(
            name='Task 1',
            description='Lorem ipsum dolor sit amet',
            deadline=timezone.now() + timezone.timedelta(minutes=30),
            priority='High',
            task_type=test_task_type
        )
        self.assertFalse(task.is_completed)

    def test_invalid_task_priority(self):
        test_task_type = TaskType.objects.create(name='Bug')
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name='Task 2',
                description='Lorem ipsum dolor sit amet',
                deadline=timezone.now() + timezone.timedelta(minutes=30),
                priority='Invalid',
                task_type=test_task_type
            )

    def test_invalid_task_deadline(self):
        test_task_type = TaskType.objects.create(name='Bug')
        with self.assertRaises(ValidationError):
            Task.objects.create(
                name='Task 3',
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


class WorkerModelTestCase(TestCase):
    def test_worker_creation(self):
        position = Position.objects.create(name='Developer')
        worker = Worker.objects.create(username='test_user', position=position)
        self.assertEqual(worker.position, position)
