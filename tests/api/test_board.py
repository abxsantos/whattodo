from typing import Tuple

import pytest

from freezegun.api import freeze_time

from whattodo.api.board import Board
from whattodo.api.task import Task


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
