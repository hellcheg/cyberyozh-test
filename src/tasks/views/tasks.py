from functools import partial
from typing import Callable

from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound as DRFNotFound
from rest_framework.exceptions import ValidationError as DRFValidationError

from tasks.models.tasks import Task, TaskStatus
from tasks.serializers.tasks import TaskSerializer
from tasks.services.tasks import assign_user, create_task, delete_task, update_status
from test_task.errors import NotFoundError, ValidationError


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: TaskSerializer):
        validated_data = serializer.validated_data
        task = create_task(
            title=validated_data["title"],
            description=validated_data["description"],
            assignee=validated_data.get("assignee", None),
        )
        serializer.instance = task


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _update(self, func: Callable[..., Task], field: str) -> Task:
        try:
            return func()
        except NotFoundError as ex:
            raise DRFNotFound(ex)
        except ValidationError as ex:
            raise DRFValidationError({field: str(ex)})

    def perform_update(self, serializer: TaskSerializer):
        validated_data = serializer.validated_data
        task_id = self.kwargs.get("pk", None)
        if assignee := validated_data.get("assignee", None):
            serializer.instance = self._update(
                partial(assign_user, task_id=task_id, user_id=assignee.id),
                field="assignee",
            )
            return
        if status := validated_data.get("status", None):
            serializer.instance = self._update(
                partial(update_status, task_id=task_id, status=TaskStatus(status)),
                field="status",
            )
            return

    def perform_destroy(self, serializer: TaskSerializer):
        task_id = self.kwargs.get("pk", None)
        try:
            delete_task(task_id=task_id)
        except NotFoundError as ex:
            raise DRFNotFound(ex)
