from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from it_company_task_manager import settings


class Position(models.Model):
    POSITION_CHOICES = (
        ('Developer', 'Developer'),
        ('Project Manager', 'Project Manager'),
        ('QA', 'QA'),
        ('Designer', 'Designer'),
        ('DevOps', 'DevOps'),
        ('HR', 'HR'),
    )

    name = models.CharField(max_length=63, choices=POSITION_CHOICES, unique=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        valid_choices = set(choice[0] for choice in self.POSITION_CHOICES)
        if self.name not in valid_choices:
            raise ValidationError({'name': 'Invalid task type name.'})


class TaskType(models.Model):
    TASK_TYPE_CHOICES = (
        ('Bug', 'Bug'),
        ('New feature', 'New feature'),
        ('QA', 'QA'),
        ('Breaking change', 'Breaking change'),
        ('Call', 'Call'),
        ("Deploy", "Deploy"),
    )

    name = models.CharField(max_length=63, choices=TASK_TYPE_CHOICES, unique=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        valid_choices = set(choice[0] for choice in self.TASK_TYPE_CHOICES)
        if self.name not in valid_choices:
            raise ValidationError({'name': 'Invalid task type name.'})


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
    min_length_validator = MinLengthValidator(limit_value=20)

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        valid_choices = set(choice[0] for choice in self.PRIORITY_CHOICES)
        if self.name not in valid_choices:
            raise ValidationError({'name': 'Invalid task type name.'})
        if self.deadline <= timezone.now():
            raise ValidationError({'deadline': 'The deadline must be in the future.'})
        if self.deadline <= timezone.now() + timezone.timedelta(minutes=10):
            raise ValidationError({'deadline': 'The deadline must be at least 10 minutes in the future.'})
