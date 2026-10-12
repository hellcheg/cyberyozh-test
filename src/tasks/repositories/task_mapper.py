from tasks.entities.task import Task
from tasks.models.tasks import Task as TaskModel


def map_model_to_task(task: TaskModel) -> Task:
    return Task.create(
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        assignee=task.assignee_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def map_task_to_model(task: Task) -> TaskModel:
    return TaskModel(
        task_id=task.task_id.value,
        title=task.title.value,
        description=task.description.value,
        status=task.status.value,
        assignee_id=task.assignee_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
