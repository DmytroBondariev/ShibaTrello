from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from task_manager.models import TaskType, Position


@receiver(post_migrate)
def create_task_types(sender, **kwargs):
    if sender.name == 'task_manager':
        TaskType.objects.all().delete()

        for choice in TaskType.TASK_TYPE_CHOICES:
            TaskType.objects.create(name=choice[0])


@receiver(post_migrate)
def create_positions(sender, **kwargs):
    if sender.name == 'task_manager':
        Position.objects.all().delete()

        for choice in Position.POSITION_CHOICES:
            Position.objects.create(name=choice[0])


@receiver(post_migrate)
def create_test_worker(sender, **kwargs):
    if sender.name == 'task_manager':
        get_user_model().objects.all().delete()
        position = Position.objects.get(name="Project Manager")
        get_user_model().objects.create_user(
            username="user",
            password="Password12345",
            first_name="lovely User",
            position=position
        )
