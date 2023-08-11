from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Position, TaskType, Worker, Task

admin.site.register(Position)

admin.site.register(TaskType)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "photo")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "email",
                        "photo",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = (
        "priority",
        "is_completed",
        "deadline",
        "task_type",
        "assignees",
    )
