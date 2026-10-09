from uuid import uuid4

import pytest

from tasks.models.tasks import TaskStatus
from tasks.services.common import get_task, get_task_for_update, get_user
from test_task.errors import NotFoundError


@pytest.mark.django_db
def test_get_task_success(task_factory):
    """Успешное получение задачи."""
    task = task_factory(status=TaskStatus.NEW, assignee=None)

    db_task = get_task(task_id=task.task_id)

    assert db_task.task_id == task.task_id


@pytest.mark.django_db
def test_get_task_not_found():
    """Задача не найдена."""
    with pytest.raises(NotFoundError):
        get_task(task_id=uuid4())


@pytest.mark.django_db
def test_get_task_for_update_success(task_factory):
    """Успешное получение задачи для апдейта."""
    task = task_factory(status=TaskStatus.NEW, assignee=None)

    db_task = get_task_for_update(task_id=task.task_id)

    assert db_task.task_id == task.task_id


@pytest.mark.django_db
def test_get_task_for_update_not_found():
    """Задача для апдейта не найдена."""
    with pytest.raises(NotFoundError):
        get_task_for_update(task_id=uuid4())


@pytest.mark.django_db
def test_get_user_success(user_factory):
    """Успешное получение пользователя."""
    user = user_factory()

    db_user = get_user(user_id=user.id)

    assert user.id == db_user.id


@pytest.mark.django_db
def test_get_user_not_found(user_factory):
    """Пользователь не найден."""
    with pytest.raises(NotFoundError):
        get_user(user_id=1)
