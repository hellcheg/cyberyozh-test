from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from tasks.models.tasks import Task
from test_task.errors import NotFoundError

User = get_user_model()


def get_task(task_id: UUID) -> Task:
    try:
        return Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise NotFoundError(f"Task ({task_id}) not found")


def get_task_for_update(task_id: UUID) -> Task:
    try:
        task = Task.objects.select_for_update().get(pk=task_id)
    except Task.DoesNotExist:
        raise NotFoundError(f"Task ({task_id}) not found")
    return task


def get_user(user_id: int) -> AbstractUser:
    try:
        new_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFoundError(f"User ({user_id}) does not exist")
    return new_user
