from rest_framework import serializers

from tasks.entities.task import TaskStatus


class TaskSerializer(serializers.Serializer):
    task_id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=TaskStatus, allow_null=True, default=None)
    assignee = serializers.IntegerField(allow_null=True, default=None)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(
        read_only=True, allow_null=True, default=True
    )


class PatchTaskSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=TaskStatus, allow_null=True, default=None)
    assignee = serializers.IntegerField(allow_null=True, default=None)
