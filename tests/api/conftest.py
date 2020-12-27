from typing import Tuple

import pytest

from whattodo.api.task import Task


@pytest.fixture(scope="function")
def make_task() -> Tuple[Task, str]:
    description = "example_description"
    result = Task(description)
    return result, description


@pytest.fixture(scope="function")
def first_task() -> Task:
    result = Task("first task")
    return result


@pytest.fixture(scope="function")
def second_task() -> Task:
    result = Task("second task")
    return result
