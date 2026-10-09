from rest_framework import generics, permissions

from tasks.serializers.tasks import CommentSerializer
from tasks.services.comments import create_comment


class TaskCommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: CommentSerializer):
        validated_data = serializer.validated_data

        comment = create_comment(
            task_id=self.kwargs.get("task_id"),
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            author_id=self.request.user.id,
        )

        serializer.instance = comment
