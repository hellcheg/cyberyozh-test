import functools
import logging
from typing import Callable

from test_task.errors import ValidationError

logger = logging.getLogger("django")


def log_domain_errors[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    Декоратор для методов сервиса.
    Логирует любые исключения, унаследованные от ValidationError, как warning.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            # Логируем имя конкретного исключения и его текст
            logger.warning(
                "Бизнес-инвариант нарушен в методе %s [%s]: %s",
                func.__name__,
                err.__class__.__name__,
                err,
            )
            raise

    return wrapper
