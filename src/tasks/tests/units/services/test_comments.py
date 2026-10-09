import pytest

from tasks.models.tasks import TaskStatus
from tasks.services.comments import create_comment
from test_task.errors import ValidationError


@pytest.mark.django_db
def test_create_comment_success(task_factory, user_factory):
    """Успешное добавления комментария к задаче."""
    task = task_factory(status=TaskStatus.NEW)
    user = user_factory()
    create_comment(
        task.task_id, title="Title", description="Description", author_id=user.id
    )
    task.refresh_from_db()
    assert len(task.comments.all()) == 1


@pytest.mark.django_db
def test_create_comment_wrong_status(task_factory, user_factory):
    """Некорректный статус задачи в которую добавляют комментарий."""
    task = task_factory(status=TaskStatus.CANCELLED)
    user = user_factory()
    with pytest.raises(ValidationError):
        create_comment(
            task.task_id, title="Title", description="Description", author_id=user.id
        )
    task.refresh_from_db()
    assert len(task.comments.all()) == 0
