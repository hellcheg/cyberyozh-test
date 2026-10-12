from typing import Callable, ContextManager

type TransactionalContext = Callable[[], ContextManager[None]]
