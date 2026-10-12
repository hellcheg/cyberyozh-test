import logging
from uuid import UUID

from tasks.entities.task import Task as TaskEntity
from tasks.entities.task import TaskStatus as TaskStatusEntity
from tasks.repositories.task_repository import TaskRepository
from tasks.services.errors_handler import log_domain_errors
from tasks.services.transaction import TransactionalContext
from test_task.errors import NotFoundError
from users.repositories import UserRepository

logger = logging.getLogger("django")


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        user_repo: UserRepository,
        transactional: TransactionalContext,
    ) -> None:
        self._task_repo = task_repo
        self._user_repo = user_repo
        self._transactional = transactional

    @log_domain_errors
    def get_all(self) -> list[TaskEntity]:
        return self._task_repo.get_all()

    @log_domain_errors
    def get_by_id(self, task_id: UUID) -> TaskEntity:
        return self._task_repo.get_by_id(task_id)

    @log_domain_errors
    def create(
        self, title: str, description: str, assignee: int | None = None
    ) -> TaskEntity:
        if assignee and not self._user_repo.exists(assignee):
            raise NotFoundError(f"User ({assignee}) does not exist")
        task = TaskEntity.create(
            title=title, description=description, status=TaskStatusEntity.NEW.value
        )
        return self._task_repo.create(task)

    @log_domain_errors
    def assign_user(self, task_id: UUID, user_id: int | None = None) -> TaskEntity:
        with self._transactional():
            task = self._task_repo.get_by_id_for_update(task_id=task_id)
            if user_id and not self._user_repo.exists(user_id):
                raise NotFoundError(f"User ({user_id}) does not exist")
            task.assign_user(user_id)
            self._task_repo.update(task)
        logger.info(f"Task {task_id} successfully reassigned to user {user_id}")
        return self._task_repo.get_by_id(task_id=task_id)

    @log_domain_errors
    def update_status(self, task_id: UUID, status: TaskStatusEntity) -> TaskEntity:
        with self._transactional():
            task = self._task_repo.get_by_id_for_update(task_id=task_id)
            old_status = task.status
            task.change_status(status)
            self._task_repo.update(task)
        logger.info(
            f"Task {task_id} status updated from {old_status} to {status.value}"
        )
        return self._task_repo.get_by_id(task_id=task_id)

    def delete_task(self, task_id: UUID) -> None:
        self._task_repo.delete_task(task_id)
        logger.info(f"Task {task_id} was permanently deleted")
        return
