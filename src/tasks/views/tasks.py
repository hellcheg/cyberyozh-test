from functools import partial
from typing import Callable
from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound as DRFNotFound
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.dependencies import container
from tasks.entities.value_objects import TaskStatus
from tasks.serializers.tasks import PatchTaskSerializer, TaskSerializer
from tasks.services.tasks import TaskEntity, TaskService
from test_task.errors import AppError, NotFoundError, ValidationError


class TaskList(APIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        with container() as request_container:
            service = request_container.get(TaskService)
            tasks = service.get_all()
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with container() as request_container:
                service = request_container.get(TaskService)
                validated_data = serializer.validated_data
                task = service.create(
                    title=validated_data["title"],
                    description=validated_data["description"],
                    assignee=validated_data.get("assignee", None),
                )
        except AppError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _update(self, func: Callable[..., TaskEntity], field: str) -> TaskEntity:
        try:
            return func()
        except NotFoundError as ex:
            raise DRFNotFound(ex)
        except ValidationError as ex:
            raise DRFValidationError({field: str(ex)})

    def get(self, request, pk: UUID) -> Response:
        with container() as request_container:
            service = request_container.get(TaskService)
            tasks = service.get_by_id(pk)
        serializer = TaskSerializer(tasks)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=PatchTaskSerializer)
    def patch(self, request, pk: UUID) -> Response:
        serializer = PatchTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        with container() as request_container:
            service = request_container.get(TaskService)
            if assignee := validated_data.get("assignee", None):
                updated_task = self._update(
                    partial(service.assign_user, task_id=pk, user_id=assignee),
                    field="assignee",
                )
            if task_status := validated_data.get("status", None):
                updated_task = self._update(
                    partial(
                        service.update_status,
                        task_id=pk,
                        status=TaskStatus(task_status),
                    ),
                    field="status",
                )

        response_serializer = TaskSerializer(updated_task)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk: UUID) -> Response:
        with container() as request_container:
            service = request_container.get(TaskService)
            try:
                service.delete_task(task_id=pk)
            except NotFoundError as err:
                return Response({"detail": str(err)}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
