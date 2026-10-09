from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

urlpatterns = [
    path("tasks/", views.TaskList.as_view(), name="task-list"),
    path("tasks/<uuid:pk>/", views.TaskDetail.as_view(), name="task-detail"),
    path(
        "tasks/<uuid:task_id>/comments/",
        views.TaskCommentViewSet.as_view({"get": "list", "post": "create"}),
        name="task-comment-list",
    ),
    path(
        "tasks/<uuid:task_id>/comments/<uuid:pk>/",
        views.TaskCommentViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="task-comment-detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
