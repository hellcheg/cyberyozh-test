from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models.tasks import Task, TaskStatus


class _TaskAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="developer", password="password123"
        )
        self.manager = User.objects.create_user(
            username="manager", password="password123"
        )

        self.list_url = reverse("task-list")

        self.client.force_authenticate(user=self.user)

        self.new_task = Task.objects.create(
            title="Тестовая задача",
            description="Описание",
            status=TaskStatus.NEW,
            assignee=self.user,
        )
        self.detail_url = reverse("task-detail", kwargs={"pk": self.new_task.pk})


class TaskAPITestsPositive(_TaskAPITests):
    def test_create_task(self):
        """Тест успешного создания задачи"""
        data = {
            "title": "Новая задача",
            "description": "Сделать тесты",
            "status": TaskStatus.NEW,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data["title"], "Новая задача")

    def test_get_tasks_list(self):
        """Тест получения списка задач"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_assign_task_to_another_user(self):
        """Тест назначения задачи другому пользователю"""
        data = {"assignee": self.manager.id}
        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.assignee, self.manager)

    def test_change_task_status(self):
        """Тест смены статуса задачи"""
        data = {"status": TaskStatus.IN_PROGRESS}
        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.status, TaskStatus.IN_PROGRESS)

    def test_mark_task_as_completed(self):
        """Тест перевода задачи в статус Выполнено"""
        response = self.client.patch(
            self.detail_url, {"status": TaskStatus.IN_PROGRESS}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.status, TaskStatus.IN_PROGRESS)
        response = self.client.patch(
            self.detail_url, {"status": TaskStatus.DONE}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.status, TaskStatus.DONE)

    def test_delete_task(self):
        """Тест удаления задачи"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class TaskAPITestsNegative(_TaskAPITests):
    def test_unauthorized_request(self):
        """Тест: неавторизованный пользователь получает 401"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_unavailable_task_status(self):
        """Тест смены статуса задачи"""
        data = {"status": TaskStatus.DONE}
        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.status, TaskStatus.NEW)

    def test_cant_assign_closed_task_to_another_user(self):
        """Тест назначения задачи другому пользователю"""
        task_status = {"status": TaskStatus.CANCELLED}
        response = self.client.patch(self.detail_url, task_status, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.status, TaskStatus.CANCELLED)
        user = {"assignee": self.manager.id}
        response = self.client.patch(self.detail_url, user, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.assignee, self.user)
