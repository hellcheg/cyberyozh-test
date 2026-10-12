import uuid

from django.db import models

from test_task import settings


# Create your models here.
class TaskStatus(models.TextChoices):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

    def get_available_next_statuses(self) -> list["TaskStatus"]:
        """Возвращает список статусов, в которые можно перейти из текущего."""
        transitions: dict[TaskStatus, list[TaskStatus]] = {
            TaskStatus.NEW: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE, TaskStatus.CANCELLED],
            TaskStatus.DONE: [],
            TaskStatus.CANCELLED: [],
        }
        return transitions.get(self, [])

    def get_closed_statuses(self) -> list["TaskStatus"]:
        return [TaskStatus.DONE, TaskStatus.CANCELLED]

    def get_opened_statuses(self) -> list["TaskStatus"]:
        return [TaskStatus.NEW, TaskStatus.IN_PROGRESS]


class Task(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
