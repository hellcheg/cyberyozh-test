from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks.views.comments import TaskCommentList
from tasks.views.tasks import TaskDetail, TaskList

urlpatterns = [
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<uuid:pk>/", TaskDetail.as_view(), name="task-detail"),
    path(
        "tasks/<uuid:task_id>/comments/",
        TaskCommentList.as_view(),
        name="task-comment-list",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
