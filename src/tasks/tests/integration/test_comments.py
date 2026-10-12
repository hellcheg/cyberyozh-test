from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models.comments import Comment
from tasks.models.tasks import Task, TaskStatus


class _CommentAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="developer", password="password123"
        )
        self.manager = User.objects.create_user(
            username="manager", password="password123"
        )

        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            title="Тестовая задача",
            description="Описание",
            status=TaskStatus.NEW,
            assignee=self.user,
        )
        self.list_url = reverse("task-comment-list", kwargs={"task_id": self.task.pk})


class CommentAPITestsPositive(_CommentAPITests):
    def test_create_comment(self):
        """Тест успешного создания комментария"""
        data = {
            "title": "Новый комментарий",
            "description": "Сделать тесты",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data["title"], "Новый комментарий")
        self.assertEqual(response.data["author"], self.user.id)
