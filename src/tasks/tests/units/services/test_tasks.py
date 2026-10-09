from uuid import uuid4

import pytest

from tasks.models.tasks import Task, TaskStatus

# Предположим, ваши сервисы лежат в модуле tasks.services
from tasks.services.tasks import assign_user, create_task, delete_task, update_status
from test_task.errors import NotFoundError, ValidationError


@pytest.mark.django_db
def test_create_task_success():
    """Успешное создание задачи"""
    task = create_task(title="Title", description="Description")
    tasks = Task.objects.all()
    assert len(tasks) == 1
    db_task = tasks[0]
    assert db_task.title == task.title


@pytest.mark.django_db
def test_create_task_with_user_success(user_factory):
    """Успешное создание задачи с указанием пользователя"""
    user = user_factory()
    task = create_task(title="Title", description="Description", assignee=user.id)
    tasks = Task.objects.all()
    assert len(tasks) == 1
    db_task = tasks[0]
    assert db_task.title == task.title


@pytest.mark.django_db
def test_delete_task_success(task_factory):
    """Успешное удаление задачи"""
    task = task_factory(status=TaskStatus.NEW, assignee=None)
    delete_task(task.task_id)
    tasks = Task.objects.all()
    assert len(tasks) == 0


@pytest.mark.django_db
def test_delete_task_not_found():
    """Задача для удаления не найдена"""
    with pytest.raises(NotFoundError):
        delete_task(uuid4())


@pytest.mark.django_db
def test_assign_user_success(task_factory, user_factory):
    """Успешное назначение пользователя"""
    task = task_factory(status=TaskStatus.NEW, assignee=None)
    user = user_factory()

    updated_task = assign_user(task_id=task.task_id, user_id=user.id)

    assert updated_task.assignee_id == user.id
    task.refresh_from_db()
    assert task.assignee_id == user.id


@pytest.mark.django_db
def test_assign_empty_user_success(task_factory):
    """Успешное убирание пользователя из задачи"""
    task = task_factory(status=TaskStatus.NEW, assignee=None)

    updated_task = assign_user(task_id=task.task_id)

    assert updated_task.assignee is None
    task.refresh_from_db()
    assert task.assignee is None


@pytest.mark.django_db
def test_assign_user_task_not_found(user_factory):
    """Не найдена задача на которую пытаются назначить пользователя"""
    user = user_factory()

    with pytest.raises(NotFoundError) as exc_info:
        assign_user(task_id=uuid4(), user_id=user.id)

    assert "not found" in str(exc_info.value)


@pytest.mark.django_db
def test_assign_user_wrong_status(task_factory, user_factory):
    """Некорректный статус у задачи на которую назначают пользователя"""
    task = task_factory(status=TaskStatus.CANCELLED, assignee=None)
    user = user_factory()

    with pytest.raises(ValidationError) as exc_info:
        assign_user(task_id=task.task_id, user_id=user.id)

    assert "Can't change assignee" in str(exc_info.value)


@pytest.mark.django_db
def test_update_status_success(task_factory):
    """Успешное изменение статуса задачи"""
    task = task_factory(status=TaskStatus.NEW)

    updated_task = update_status(task_id=task.task_id, status=TaskStatus.IN_PROGRESS)

    assert updated_task.status == TaskStatus.IN_PROGRESS
    task.refresh_from_db()
    assert task.status == TaskStatus.IN_PROGRESS


@pytest.mark.django_db
def test_update_status_validation_error(task_factory):
    """Некорректный статус у задачи для изменения"""
    task = task_factory(status=TaskStatus.DONE)

    with pytest.raises(ValidationError):
        update_status(task_id=task.task_id, status=TaskStatus.NEW)
