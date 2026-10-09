from uuid import UUID

from tasks.models.comments import Comment
from tasks.models.tasks import TaskStatus
from tasks.services.common import get_task, get_user
from tasks.services.tasks import ValidationError


def create_comment(
    task_id: UUID, title: str, description: str, author_id: int
) -> Comment:
    task = get_task(task_id)
    current_status = TaskStatus(task.status)
    if current_status in current_status.get_closed_statuses():
        raise ValidationError("Can't comment closed task")
    author = get_user(author_id)
    new_comment = Comment(
        title=title, description=description, task_id=task.task_id, author_id=author.pk
    )
    new_comment.save()
    return new_comment
