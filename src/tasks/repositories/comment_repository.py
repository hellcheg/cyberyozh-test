from uuid import UUID

from tasks.entities.comment import Comment
from tasks.models.comments import Comment as CommentModel
from tasks.repositories.comment_mapper import map_comment_to_model, map_model_to_comment


class CommentRepository:
    def get_tasks_comments(self, task_id: UUID) -> list[Comment]:
        queryset = CommentModel.objects.filter(task_id=task_id)
        return [map_model_to_comment(task) for task in queryset]

    def create_comment(self, comment: Comment) -> Comment:
        new_comment = map_comment_to_model(comment)
        new_comment.save()
        return map_model_to_comment(new_comment)
