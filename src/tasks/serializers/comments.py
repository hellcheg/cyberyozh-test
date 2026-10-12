from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    task_id = serializers.UUIDField(read_only=True)
    author = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(
        read_only=True, allow_null=True, default=True
    )
