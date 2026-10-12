from tasks.entities.comment import Comment
from tasks.models.comments import Comment as CommentModel


def map_model_to_comment(comment: CommentModel) -> Comment:
    return Comment.create(
        comment_id=comment.comment_id,
        task_id=comment.task_id,
        title=comment.title,
        description=comment.description,
        author=comment.author_id,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


def map_comment_to_model(comment: Comment) -> CommentModel:
    return CommentModel(
        comment_id=comment.comment_id.value,
        task_id=comment.task_id.value,
        title=comment.title.value,
        description=comment.description.value,
        author_id=comment.author,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )
