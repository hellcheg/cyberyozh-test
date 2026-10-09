from pytest_factoryboy import register

# Укажите правильный импорт ваших фабрик
from tasks.tests.units.factories import TaskFactory, UserFactory

register(TaskFactory)
register(UserFactory)
