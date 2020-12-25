from datetime import datetime
from typing import Tuple

import pytest
from freezegun.api import freeze_time
from src.api import Task


@pytest.fixture(scope="function")
def make_task() -> Tuple[Task, str]:
    description = "example_description"
    result = Task(description)
    return result, description


@pytest.mark.smoke
def test_task_must_have_description(make_task):
    task, example_description = make_task
    assert task.description == example_description


@pytest.mark.smoke
@freeze_time("2020-12-25")
def test_task_must_have_a_created_at(make_task):
    task = make_task
    assert task.created_at == datetime.now()


@pytest.mark.smoke
def test_task_status_must_be_false_as_default(make_task):
    task, _ = make_task
    assert task._status is False
    assert task.status == "✘"


@pytest.mark.parametrize(
    "param_value, expected_value, unicode_repr",
    [
        ("done", True, "ކ"),
        ("banana", False, "✘"),
    ],
)
def test_task_status_can_be_altered_to_true_given_correct_value(
    make_task, param_value: bool, expected_value: bool, unicode_repr: str
):
    task, _ = make_task
    task.status = param_value
    assert task._status is expected_value
    assert task.status == unicode_repr


@pytest.mark.parametrize(
    "param_value, expected_value, unicode_repr",
    [
        ("done", True, "ކ"),
        ("banana", True, "ކ"),
        ("not done", False, "✘"),
    ],
)
def test_task_can_be_altered_to_false_given_correct_value(
    make_task, param_value: bool, expected_value: bool, unicode_repr: str
):
    task, _ = make_task
    task._status = True
    task.status = param_value
    assert task._status is expected_value
    assert task.status == unicode_repr
