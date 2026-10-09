from rest_framework import serializers

from tasks.models.tasks import Task
from tasks.serializers.comments import CommentSerializer


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "task_id",
            "title",
            "description",
            "status",
            "assignee",
            "comments",
            "created_at",
            "updated_at",
        ]
