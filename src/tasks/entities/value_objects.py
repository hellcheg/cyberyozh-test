from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4

from test_task.errors import ValidationError

TITLE_LENGHT = 255


@dataclass(frozen=True)
class ValueObject[T]:
    value: T

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(ValueObject[str]):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) > TITLE_LENGHT:
            raise ValidationError(f"The title cannot exceed {TITLE_LENGHT} characters.")
        if len(self.value) <= 0:
            raise ValidationError("The title field cannot be empty.")


@dataclass(frozen=True)
class Description(ValueObject[str]):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) <= 0:
            raise ValidationError("The description field cannot be empty.")


@dataclass(frozen=True)
class EntityId(ValueObject[UUID]):
    value: UUID = field(default_factory=uuid4)

    @classmethod
    def from_string(cls, entity_id: str) -> "EntityId":
        try:
            return cls(value=UUID(entity_id))
        except ValueError:
            raise ValueError(f"Некорректный формат UUID: {entity_id}")


class TaskStatus(StrEnum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

    def can_transition_to(self, next_status: "TaskStatus") -> bool:
        allowed_transitions: dict[TaskStatus, list[TaskStatus]] = {
            TaskStatus.NEW: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE, TaskStatus.CANCELLED],
            TaskStatus.DONE: [],
            TaskStatus.CANCELLED: [],
        }
        return next_status in allowed_transitions[self]

    @property
    def allows_assignment(self) -> bool:
        return self in (TaskStatus.NEW, TaskStatus.IN_PROGRESS)

    @property
    def allows_commenting(self) -> bool:
        return self in (TaskStatus.NEW, TaskStatus.IN_PROGRESS)
