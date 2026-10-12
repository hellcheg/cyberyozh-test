from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from tasks.entities.comment import Comment
from tasks.entities.value_objects import Description, EntityId, TaskStatus, Title
from test_task.errors import ValidationError


@dataclass
class Task:
    task_id: EntityId
    title: Title
    description: Description
    status: TaskStatus
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        status: str,
        task_id: UUID | None = None,
        assignee: int | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> "Task":
        new_id = EntityId(task_id) if task_id else EntityId()
        return cls(
            task_id=new_id,
            title=Title(title),
            description=Description(description),
            status=TaskStatus(status),
            assignee_id=assignee,
            created_at=created_at or datetime.now(tz=UTC),
            updated_at=updated_at,
        )

    def change_status(self, status: TaskStatus) -> Self:
        if not self.status.can_transition_to(status):
            raise ValidationError(f"Can't change status from {self.status} to {status}")
        self.status = status
        self.updated_at = datetime.now(tz=UTC)
        return self

    def assign_user(self, assignee_id: int | None) -> Self:
        if self.assignee_id != assignee_id and not self.status.allows_assignment:
            raise ValidationError(f"Can't change assignee in status {self.status}")
        self.assignee_id = assignee_id
        self.updated_at = datetime.now(tz=UTC)
        return self

    def create_comment(self, title: str, description: str, author: int) -> Comment:
        if not self.status.allows_commenting:
            raise ValidationError("Can't comment closed task")
        return Comment.create(
            task_id=self.task_id.value,
            title=title,
            description=description,
            author=author,
        )
