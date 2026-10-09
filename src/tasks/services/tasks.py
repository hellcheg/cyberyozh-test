import logging
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.db import transaction

from tasks.models.tasks import Task, TaskStatus
from tasks.services.common import get_task, get_task_for_update, get_user
from tasks.validators import can_assign_user, is_status_available
from test_task.errors import ValidationError

logger = logging.getLogger("django")


def create_task(title: str, description: str, assignee: int | None = None) -> Task:
    user: AbstractUser | None = None
    if assignee:
        user = get_user(assignee)

    new_task = Task(
        title=title,
        description=description,
        assignee=user,
        status=TaskStatus.NEW,
    )
    new_task.save()
    return new_task


@transaction.atomic
def assign_user(task_id: UUID, user_id: int | None = None) -> Task:
    task = get_task_for_update(task_id)
    if user_id is None:
        task.assignee = None
        task.save()
        return task

    new_user = get_user(user_id)

    if not can_assign_user(task.assignee_id, new_user.id, TaskStatus(task.status)):
        logger.warning(
            f"Validation failed: Can't assign user {user_id} to task {task_id}. Current status: {task.status}"
        )
        raise ValidationError(f"Can't change assignee in status123123 {task.status}")

    task.assignee = new_user
    task.save()
    logger.info(f"Task {task_id} successfully reassigned to user {user_id}")
    return task


@transaction.atomic
def update_status(task_id: UUID, status: TaskStatus) -> Task:
    task = get_task_for_update(task_id)

    if not is_status_available(TaskStatus(task.status), status):
        logger.warning(
            f"Validation failed: Forbidden status transition for task {task_id} from {task.status} to {status.value}"
        )
        raise ValidationError(
            f"Can't change status from {task.status} to {status.value}"
        )
    old_status = task.status
    task.status = status.value
    task.save()
    logger.info(f"Task {task_id} status updated from {old_status} to {status.value}")
    return task


@transaction.atomic
def delete_task(task_id: UUID) -> None:
    task = get_task(task_id)
    task.delete()
    logger.info(f"Task {task_id} was permanently deleted")
    return
