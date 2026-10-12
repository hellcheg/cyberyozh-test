from contextlib import contextmanager

from dishka import Provider, Scope, make_container, provide
from django.db import transaction

from tasks.repositories.comment_repository import CommentRepository
from tasks.repositories.task_repository import TaskRepository
from tasks.services.comments import CommentService
from tasks.services.tasks import TaskService
from tasks.services.transaction import TransactionalContext
from users.repositories import UserRepository


class AppProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_task_repo(self) -> TaskRepository:
        return TaskRepository()

    @provide
    def get_user_repo(self) -> UserRepository:
        return UserRepository()

    @provide
    def get_comment_repo(self) -> CommentRepository:
        return CommentRepository()

    @provide
    def get_task_service(
        self,
        task_repo: TaskRepository,
        user_repo: UserRepository,
        transactional: TransactionalContext,
    ) -> TaskService:
        return TaskService(task_repo, user_repo, transactional)

    @provide
    def get_comment_service(
        self,
        comment_repo: CommentRepository,
        task_repo: TaskRepository,
        user_repo: UserRepository,
    ) -> CommentService:
        return CommentService(comment_repo, task_repo, user_repo)

    @provide(scope=Scope.APP)
    def get_transactional_context(self) -> TransactionalContext:
        @contextmanager
        def _transaction():
            with transaction.atomic():
                yield

        return _transaction


container = make_container(AppProvider())
