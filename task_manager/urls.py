from django.urls import path

from task_manager.views import (
    IndexView, WorkerListView, UserLoginView,
    TaskListView, WorkerDetailView, TaskCreateView, TaskUpdateView,
    TaskDetailView, WorkerCreateView, WorkerUpdateView,
    ToggleAssignToTaskView, WorkerDeleteView, UserLogoutView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        ToggleAssignToTaskView.as_view(),
        name="toggle-task-assign",
    ),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
]

app_name = "task_manager"
