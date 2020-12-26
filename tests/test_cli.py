from unittest.mock import patch

import pytest

from freezegun.api import freeze_time
from typer.testing import CliRunner

from whattodo.api.board import Board
from whattodo.cli import app


@pytest.mark.smoke
def test_whattodo_cli_entrypoint():
    runner = CliRunner()
    result = runner.invoke(app, [])

    assert result.exit_code == 0

    assert "WhatTodo" in result.output


@patch("whattodo.cli.store_to_json")
def test_add_board_cli_command(mocked_store_to_json):
    runner = CliRunner()
    board_name = "personal"

    result = runner.invoke(app, ["board:add", board_name])

    assert result.exit_code == 0
    assert board_name in result.output
    mocked_store_to_json.assert_called_once_with(data={"name": board_name, "tasks": []})


@patch("whattodo.cli.read_from_json")
def test_list_board_tasks_cli_command(mocked_read_from_json):
    runner = CliRunner()
    board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    task_list = Board.from_dict(board_dict).list_tasks
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:list"])

    assert result.exit_code == 0
    assert result.output == task_list + "\n"


@patch("whattodo.cli.read_from_json")
def test_count_board_tasks_cli_command(mocked_read_from_json):
    runner = CliRunner()
    board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    count = Board.from_dict(board_dict).count_tasks
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:count"])

    assert result.exit_code == 0
    assert str(count) in result.output


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_add_task_cli_command(mocked_read_from_json, mocked_store_to_json):
    with freeze_time("2020-12-26 00:00:00"):
        runner = CliRunner()
        task_description = "my added task"
        board_dict = {
            "name": "personal",
            "tasks": [
                {
                    "description": "my first task",
                    "status": False,
                    "created_at": "2020-12-26 15:13:45",
                },
                {
                    "description": "my second task",
                    "status": False,
                    "created_at": "2020-12-26 15:13:56",
                },
            ],
        }
        expected_board_dict = {
            "name": "personal",
            "tasks": [
                {
                    "description": "my first task",
                    "status": False,
                    "created_at": "2020-12-26 15:13:45",
                },
                {
                    "description": "my second task",
                    "status": False,
                    "created_at": "2020-12-26 15:13:56",
                },
                {
                    "description": "my added task",
                    "status": False,
                    "created_at": "2020-12-26 00:00:00",
                },
            ],
        }
        mocked_read_from_json.return_value = board_dict

        result = runner.invoke(app, ["task:add", task_description])

        assert result.exit_code == 0
        assert task_description in result.output
        mocked_store_to_json.assert_called_once_with(expected_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_update_task_cli_command(mocked_read_from_json, mocked_store_to_json):
    runner = CliRunner()
    task_description = "my added task"
    board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    expected_board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": True,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["task:update", "done", "1"])

    assert result.exit_code == 0
    assert "done" in result.output
    mocked_store_to_json.assert_called_once_with(expected_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_clean_board_cli_command(mocked_read_from_json, mocked_store_to_json):
    runner = CliRunner()
    board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    expected_board_dict = {
        "name": "personal",
        "tasks": [],
    }
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:clean"], input="y\n")

    assert result.exit_code == 0
    mocked_store_to_json.assert_called_once_with(expected_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_remove_task_cli_command(mocked_read_from_json, mocked_store_to_json):
    runner = CliRunner()
    board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }
    expected_board_dict = {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
        ],
    }
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["task:remove", "1"], input="y\n")

    assert result.exit_code == 0
    mocked_store_to_json.assert_called_once_with(expected_board_dict)
