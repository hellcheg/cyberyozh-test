from __future__ import annotations

from tasks.models import TaskStatus


def is_status_available(current: TaskStatus, new: TaskStatus) -> bool:
    available_statuses = current.get_available_next_statuses()
    return current == new or new in available_statuses


def can_assign_user(current_user_id: int, new_user_id: int, status: TaskStatus) -> bool:
    return current_user_id == new_user_id or status in status.get_opened_statuses()
