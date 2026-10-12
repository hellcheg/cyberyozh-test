from uuid import UUID

from tasks.entities.task import Task
from tasks.models.tasks import Task as TaskModel
from tasks.repositories.task_mapper import map_model_to_task, map_task_to_model
from test_task.errors import NotFoundError


class TaskRepository:
    def get_all(self) -> list[Task]:
        queryset = TaskModel.objects.all()
        return [map_model_to_task(task) for task in queryset]

    def get_by_id(self, task_id: UUID) -> Task:
        try:
            task = TaskModel.objects.get(pk=task_id)
        except TaskModel.DoesNotExist:
            raise NotFoundError(f"Task ({task_id}) not found")
        return map_model_to_task(task)

    def get_by_id_for_update(self, task_id: UUID) -> Task:
        try:
            task = TaskModel.objects.select_for_update().get(pk=task_id)
        except TaskModel.DoesNotExist:
            raise NotFoundError(f"Task ({task_id}) not found")
        return map_model_to_task(task)

    def create(self, task: Task) -> Task:
        new_task = map_task_to_model(task)
        new_task.save()
        return map_model_to_task(new_task)

    def update(self, task: Task):
        TaskModel.objects.filter(task_id=task.task_id.value).update(
            status=task.status,
            assignee_id=task.assignee_id,
            updated_at=task.updated_at,
        )

    def delete_task(self, task_id: UUID):
        try:
            task = TaskModel.objects.get(pk=task_id)
        except TaskModel.DoesNotExist:
            raise NotFoundError(f"Task ({task_id}) not found")
        task.delete()
