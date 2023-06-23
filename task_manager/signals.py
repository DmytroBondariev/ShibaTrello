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
