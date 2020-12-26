from datetime import datetime
from typing import Tuple

import pytest

from freezegun.api import freeze_time

from whattodo.api import Board
from whattodo.api import Task


@pytest.fixture(scope="function")
def make_task() -> Tuple[Task, str]:
    description = "example_description"
    result = Task(description)
    return result, description


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


class TestBoard:
    @pytest.mark.smoke
    def test_board_must_have_a_name(self):
        board = Board(name="personal")
        assert board.name == "personal"

    def test_board_must_hold_added_tasks(self, make_task: Tuple[Task, str]):
        task, _ = make_task
        board = Board(name="personal")
        board.add(task)
        assert len(board.tasks) == 1
        assert board.tasks.pop() == task

    def test_list_tasks_must_retrieve_tasks_description_status_and_created_date(
        self, make_task: Tuple[Task, str]
    ):
        task, _ = make_task
        board = Board(name="personal")
        board.add(task)
        assert "No tasks on this board!" not in board.list_tasks
        assert task.description in board.list_tasks
        assert task.status in board.list_tasks
        assert task.created_at in board.list_tasks

    def test_list_tasks_must_return_an_empty_board_representation_when_no_tasks(self):
        board = Board(name="personal")
        assert "No tasks on this board!" in board.list_tasks

    def test_count_tasks_must_return_the_number_of_tasks_on_the_board(
        self, make_task: Tuple[Task, str]
    ):
        task, _ = make_task
        board = Board(name="personal")
        board.add(task)
        assert board.count_tasks == 1
        board.add(task)
        assert board.count_tasks == 2

    def test_retrieve_task_must_retrieve_the_correct_task(self):
        first_task = Task("first task")
        second_task = Task("second task")
        board = Board(name="personal")
        board.add(first_task)
        board.add(second_task)
        assert board.retrieve_task(0) == first_task
        assert board.retrieve_task(1) == second_task

    def test_retrieve_task_must_raise_value_error_when_no_tasks_are_on_board(self):
        board = Board(name="personal")
        with pytest.raises(ValueError) as excinfo:
            board.retrieve_task(0)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "No tasks on this board!"

    def test_retrieve_task_must_raise_index_error_given_invalid_index(self):
        first_task = Task("first task")
        board = Board(name="personal")
        board.add(first_task)
        index = 1
        with pytest.raises(IndexError) as excinfo:
            board.retrieve_task(index)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == f"No tasks found at the index {index}"

    @pytest.mark.smoke
    def test_board_must_have_str_representation(self):
        board = Board(name="personal")
        assert str(board) == board.list_tasks

    @pytest.mark.smoke
    def test_board_must_have_repr_representation(self):
        board = Board(name="personal")
        assert repr(board) == f"<Board {board.name} >"

    def test_from_dict(self):
        board_dict = {
            "name": "personal",
            "tasks": [
                {
                    "description": "my first task",
                    "status": False,
                    "created_at": "2020-12-26 00:00:00",
                },
                {
                    "description": "my second task",
                    "status": True,
                    "created_at": "2020-12-26 00:01:00",
                },
            ],
        }

        board = Board.from_dict(dict_board=board_dict)

        assert isinstance(board, Board)
        assert board.name == board_dict["name"]
        assert board.count_tasks == 2
        assert isinstance(board.retrieve_task(0), Task)
        assert isinstance(board.retrieve_task(1), Task)

    def test_to_dict(self):
        with freeze_time("2020-12-26 00:00:00"):
            board_dict = {
                "name": "personal",
                "tasks": [
                    {
                        "description": "my first task",
                        "status": False,
                        "created_at": "2020-12-26 00:00:00",
                    },
                    {
                        "description": "my second task",
                        "status": True,
                        "created_at": "2020-12-26 00:00:00",
                    },
                ],
            }

            first_task = Task("my first task")
            second_task = Task("my second task")
            second_task._status = True
            board = Board(name="personal")
            board.add(first_task)
            board.add(second_task)

            assert board.to_dict() == board_dict
