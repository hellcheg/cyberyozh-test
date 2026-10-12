import pytest

from tasks.entities.task import Title
from test_task.errors import ValidationError


@pytest.mark.parametrize("title", ["Test", "T" * 200])
def test_title_success(title: str):
    new_title = Title(value=title)
    assert new_title.value == title


@pytest.mark.parametrize(
    "title",
    ["", "a" * 1000],
)
def test_title_error(title: str):
    with pytest.raises(ValidationError):
        Title(value=title)
