import pytest

# Укажите правильный импорт ваших фабрик
from tasks.entities.task import Task


@pytest.fixture
def task() -> Task:
    return Task.create(
        title="Test title",
        description="Test description",
        status="NEW",
    )
