import factory

from tasks.models.tasks import Task, TaskStatus


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.CustomUser"

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    status = TaskStatus.NEW
    assignee = None
