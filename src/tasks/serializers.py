from django.shortcuts import get_object_or_404
from rest_framework import serializers

from tasks.models import Comment, Task, TaskStatus
from tasks.validators import can_assign_user, is_status_available


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "task",
            "title",
            "description",
            "author",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        view = self.context["view"]
        task_id = view.kwargs.get("task_id")

        # 2. Находим задачу
        task = get_object_or_404(Task, task_id=task_id)
        current_status = TaskStatus(task.status)
        if current_status in current_status.get_closed_statuses():
            raise serializers.ValidationError({"assignee": "Can't comment closed task"})
        attrs["task"] = task
        return attrs


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

    def validate(self, attrs):
        new_status = attrs.get("status", None)
        new_assignee = attrs.get("assignee", None)

        if self.instance:
            current_status = self.instance.status
            if new_status and not is_status_available(
                TaskStatus(current_status), TaskStatus(new_status)
            ):
                raise serializers.ValidationError(
                    {
                        "status": f"Can't change status from {current_status} to {new_status}"
                    }
                )
            if new_assignee and not can_assign_user(
                self.instance.assignee, new_assignee, TaskStatus(current_status)
            ):
                raise serializers.ValidationError(
                    {
                        "assignee": f"Can't change change assignee in status {current_status}"
                    }
                )
        return attrs
