from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from tasks.entities.task import Task, TaskStatus
from test_task.errors import ValidationError


@pytest.mark.parametrize(
    "task_id",
    [None, uuid4()],
)
def test_create_task_with_different_ids(task_id: UUID | None):
    task = Task.create(
        title="Title", description="Description", status="NEW", task_id=task_id
    )
    assert isinstance(task.task_id.value, UUID)


@pytest.mark.parametrize(
    "created_at",
    [None, datetime.now(tz=UTC)],
)
def test_create_task_with_different_created_at(created_at: datetime | None):
    task = Task.create(
        title="Title", description="Description", status="NEW", created_at=created_at
    )
    assert isinstance(task.created_at, datetime)


@pytest.mark.parametrize(
    "status, old_user, new_user",
    [
        (TaskStatus.NEW, 1, 1),
        (TaskStatus.IN_PROGRESS, 1, 1),
        (TaskStatus.NEW, 1, None),
        (TaskStatus.IN_PROGRESS, 1, None),
        (TaskStatus.NEW, None, None),
        (TaskStatus.IN_PROGRESS, None, None),
        (TaskStatus.NEW, None, 2),
        (TaskStatus.IN_PROGRESS, None, 2),
        (TaskStatus.DONE, 2, 2),
        (TaskStatus.CANCELLED, 2, 2),
    ],
)
def test_assign_user_success(
    task: Task, status: TaskStatus, old_user: int | None, new_user: int | None
):
    task.status = status
    task.assignee_id = old_user
    task.assign_user(new_user)
    assert task.assignee_id == new_user


@pytest.mark.parametrize(
    "status, old_user, new_user",
    [
        (TaskStatus.DONE, 1, 2),
        (TaskStatus.CANCELLED, 1, 2),
        (TaskStatus.DONE, 1, None),
        (TaskStatus.CANCELLED, 1, None),
    ],
)
def test_assign_user_wrong_status(
    task: Task, status: TaskStatus, old_user: int, new_user: int | None
):
    task.status = status
    task.assignee_id = old_user
    with pytest.raises(ValidationError):
        task.assign_user(new_user)


@pytest.mark.parametrize(
    "old_status, new_status",
    [
        (TaskStatus.NEW, TaskStatus.IN_PROGRESS),
        (TaskStatus.NEW, TaskStatus.CANCELLED),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED),
    ],
)
def test_change_status_success(
    task: Task, old_status: TaskStatus, new_status: TaskStatus
):
    task.status = old_status
    task.change_status(new_status)
    assert task.status == new_status


@pytest.mark.parametrize(
    "old_status, new_status",
    [
        (TaskStatus.NEW, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.NEW),
        (TaskStatus.DONE, TaskStatus.NEW),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
        (TaskStatus.CANCELLED, TaskStatus.NEW),
        (TaskStatus.CANCELLED, TaskStatus.IN_PROGRESS),
    ],
)
def test_change_status_wrong_status(
    task: Task, old_status: TaskStatus, new_status: TaskStatus
):
    task.status = old_status
    with pytest.raises(ValidationError):
        task.change_status(new_status)


def test_create_comment_success(task: Task):
    comment = task.create_comment(
        title="Comment title",
        description="Comment description",
        author=1,
    )
    assert comment.task_id == task.task_id


@pytest.mark.parametrize(
    "status",
    [TaskStatus.DONE, TaskStatus.CANCELLED],
)
def test_create_comment_wrong_status(task: Task, status: TaskStatus):
    task.status = status
    with pytest.raises(ValidationError):
        task.create_comment(
            title="Comment title",
            description="Comment description",
            author=1,
        )
