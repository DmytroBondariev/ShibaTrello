from django.contrib.auth.models import AbstractUser
from django.db import models

from it_company_task_manager import settings


class Position(models.Model):
    POSITION_CHOICES = [
        ('Developer', 'Developer'),
        ('Project Manager', 'Project Manager'),
        ('QA', 'QA'),
        ('Designer', 'Designer'),
        ('DevOps', 'DevOps'),
        ('HR', 'HR'),
    ]

    name = models.CharField(max_length=63, choices=POSITION_CHOICES, unique=True)


class TaskType(models.Model):
    TASK_TYPE_CHOICES = [
        ('Bug', 'Bug'),
        ('New feature', 'New feature'),
        ('QA', 'QA'),
        ('Breaking change', 'Breaking change'),
        ('Call', 'Call'),
        ("Deploy", "Deploy"),
    ]

    name = models.CharField(max_length=63, choices=TASK_TYPE_CHOICES, unique=True)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name}, position: {self.position.name})"


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', '***'),
        ('High', '**'),
        ("Average", "*"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=63, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return f"Task number: {self.id}. Topic: {self.name}"
