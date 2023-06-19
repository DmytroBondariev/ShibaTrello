from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path

from task_manager.views import index, WorkerListView, UserLoginView, logout_view, UserPasswordChangeView, \
    UserPasswordResetView, UserPasswordResetConfirmView, TaskListView, WorkerDetailView, TaskCreateView, TaskUpdateView, \
    TaskDetailView, WorkerCreateView, WorkerUpdateView, toggle_assign_to_task

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path(
        "tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

]

app_name = "task_manager"
