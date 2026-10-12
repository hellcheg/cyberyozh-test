from uuid import UUID

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.dependencies import container
from tasks.serializers.comments import CommentSerializer
from tasks.services.comments import CommentService
from test_task.errors import AppError


class TaskCommentList(APIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, task_id: UUID) -> Response:
        with container() as request_container:
            service = request_container.get(CommentService)
            comments = service.get_tasks_comments(task_id)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, task_id: UUID) -> Response:
        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            current_user = request.user
            with container() as request_container:
                service = request_container.get(CommentService)
                validated_data = serializer.validated_data
                task = service.create(
                    task_id=task_id,
                    title=validated_data["title"],
                    description=validated_data["description"],
                    author=current_user.id,
                )
        except AppError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = CommentSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
