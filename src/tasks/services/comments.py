from uuid import UUID

from tasks.entities.comment import Comment
from tasks.models.comments import Comment as CommentModel
from tasks.models.tasks import TaskStatus
from tasks.repositories.comment_repository import CommentRepository
from tasks.repositories.task_repository import TaskRepository
from tasks.services.common import get_task, get_user
from test_task.errors import NotFoundError, ValidationError
from users.repositories import UserRepository


def create_comment(
    task_id: UUID, title: str, description: str, author_id: int
) -> CommentModel:
    task = get_task(task_id)
    current_status = TaskStatus(task.status)
    if current_status in current_status.get_closed_statuses():
        raise ValidationError("Can't comment closed task")
    author = get_user(author_id)
    new_comment = CommentModel(
        title=title, description=description, task_id=task.task_id, author_id=author.pk
    )
    new_comment.save()
    return new_comment


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository,
        task_repo: TaskRepository,
        user_repo: UserRepository,
    ):
        self._comment_repo = comment_repo
        self._task_repo = task_repo
        self._user_repo = user_repo

    def get_tasks_comments(self, task_id: UUID) -> list[Comment]:
        return self._comment_repo.get_tasks_comments(task_id)

    def create(
        self, task_id: UUID, title: str, description: str, author: int
    ) -> Comment:
        task = self._task_repo.get_by_id(task_id)
        if not self._user_repo.exists(author):
            raise NotFoundError(f"User ({author}) does not exist")
        comment = task.create_comment(title, description, author)
        return self._comment_repo.create_comment(comment)
