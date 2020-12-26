from datetime import datetime
from typing import Tuple

import pytest

from freezegun.api import freeze_time

from whattodo.api.task import Task


class TestTask:
    @pytest.mark.smoke
    def test_task_must_have_description(self, make_task: Tuple[Task, str]):
        task, example_description = make_task
        assert task.description == example_description

    @pytest.mark.smoke
    def test_task_must_have_a_created_at(self):
        with freeze_time("2020-12-25"):
            task = Task("example_description")
            assert task.created_at == datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @pytest.mark.smoke
    def test_task_status_must_be_false_as_default(self, make_task: Tuple[Task, str]):
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
        self,
        make_task: Tuple[Task, str],
        param_value: str,
        expected_value: bool,
        unicode_repr: str,
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
        self,
        make_task: Tuple[Task, str],
        param_value: str,
        expected_value: bool,
        unicode_repr: str,
    ):
        task, _ = make_task
        task._status = True
        task.status = param_value
        assert task._status is expected_value
        assert task.status == unicode_repr

    def test_task_description_can_be_updated(self, make_task: Tuple[Task, str]):
        task, old_description = make_task
        task.description = "my new description"
        assert task.description != old_description

    @pytest.mark.smoke
    def test_task_must_have_str_representation(self, make_task: Tuple[Task, str]):
        task, description = make_task
        assert str(task) == f"{description} {task.status}"

    @pytest.mark.smoke
    def test_task_must_have_repr_representation(self, make_task: Tuple[Task, str]):
        task, description = make_task
        assert repr(task) == f"<Task {description} >"

    def test_from_dict(self):
        task_dict = {
            "description": "my first task",
            "status": False,
            "created_at": "2020-12-26 00:00:00",
        }

        task = Task.from_dict(dict_task=task_dict)

        assert isinstance(task, Task)
        assert task.description == "my first task"
        assert task._status is False
        assert isinstance(task._created_at, datetime)
        assert task.created_at == "2020-12-26 00:00:00"

    def test_to_dict(self):
        task_dict = {
            "description": "my first task",
            "status": False,
            "created_at": "2020-12-26 00:00:00",
        }

        with freeze_time("2020-12-26 00:00:00"):
            task = Task(description="my first task")
            assert task.to_dict() == task_dict
