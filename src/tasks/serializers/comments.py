from rest_framework import serializers

from tasks.models.comments import Comment


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
