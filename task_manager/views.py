from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic

from task_manager.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, \
    WorkerSearchForm, TaskSearchForm, TaskForm
from task_manager.models import Position, Task, TaskType, Worker


def index(request):
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_positions": num_positions,
        "num_task_types": num_task_types,
        "num_visits": num_visits
    }
    return render(request=request, template_name='pages/index.html', context=context)


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 6
    template_name = "pages/worker_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = WorkerSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["name"]
            )
        return queryset


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks__task_type")
    template_name = "pages/worker_detail.html"


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.all()
    template_name = "pages/task_detail.html"


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "pages/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related("assignees")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskCreateView(generic.CreateView):
    fields = ("task_type", "name", "description", "deadline", "priority", "assignees")
    model = Task
    # form_class = TaskForm
    template_name = "pages/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "pages/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_manager:index')


def logout_view(request):
    logout(request)
    return redirect('/')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
