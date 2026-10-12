from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from tasks.entities.value_objects import Description, EntityId, Title


@dataclass
class Comment:
    comment_id: EntityId
    task_id: EntityId
    title: Title
    description: Description
    author: int
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def create(
        cls,
        task_id: UUID,
        title: str,
        description: str,
        author: int,
        comment_id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> "Comment":
        new_id = EntityId(comment_id) if comment_id else EntityId()
        new_task_id = EntityId(task_id)
        return cls(
            comment_id=new_id,
            task_id=new_task_id,
            title=Title(title),
            description=Description(description),
            author=author,
            created_at=created_at or datetime.now(tz=UTC),
            updated_at=updated_at,
        )
