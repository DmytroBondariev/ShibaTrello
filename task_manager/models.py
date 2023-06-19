from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
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
        ("CEO", "CEO"),
    )

    name = models.CharField(max_length=63, choices=POSITION_CHOICES, unique=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.RESTRICT, null=True)
    photo = models.ImageField(upload_to='workers_photo', null=True, blank=True)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["-position"]

    def __str__(self):
        return f"{self.username} " \
               f"({self.first_name} {self.last_name}, " \
               f"position: {self.position.name if self.position else None})"

    def get_absolute_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.id})


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', '***'),
        ('High', '**'),
        ("Average", "*"),
    ]
    min_length_validator = MinLengthValidator(limit_value=10)

    name = models.CharField(max_length=100, unique=True, validators=[min_length_validator])
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=63, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["-priority"]

    def __str__(self):
        return f"Task number: {self.id}. Topic: {self.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.deadline <= timezone.now():
            raise ValidationError({'deadline': 'The deadline must be in the future.'})

        if self.deadline <= timezone.now() + timezone.timedelta(minutes=10):
            raise ValidationError({'deadline': 'The deadline must be at least 10 minutes in the future.'})

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", kwargs={"pk": self.id})
