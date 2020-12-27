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
    board_name = "personal"
    runner = CliRunner()
    result = runner.invoke(app, ["board:add", board_name])

    assert result.exit_code == 0
    assert board_name in result.output
    mocked_store_to_json.assert_called_once_with(data={"name": board_name, "tasks": []})


@patch("whattodo.cli.read_from_json")
def test_list_board_tasks_cli_command(mocked_read_from_json, board_dict):
    runner = CliRunner()
    task_list = Board.from_dict(board_dict).list_tasks
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:list"])

    assert result.exit_code == 0
    assert result.output == task_list + "\n"


@patch("whattodo.cli.read_from_json")
def test_count_board_tasks_cli_command(mocked_read_from_json, board_dict):
    runner = CliRunner()
    count = Board.from_dict(board_dict).count_tasks
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:count"])

    assert result.exit_code == 0
    assert str(count) in result.output


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_add_task_cli_command(
    mocked_read_from_json, mocked_store_to_json, board_dict, expected_board_dict
):
    task_description = "my added task"
    with freeze_time("2020-12-26 00:00:00"):
        runner = CliRunner()
        mocked_read_from_json.return_value = board_dict

        result = runner.invoke(app, ["task:add", task_description])

        assert result.exit_code == 0
        assert task_description in result.output
        mocked_store_to_json.assert_called_once_with(expected_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_update_task_cli_command(
    mocked_read_from_json,
    mocked_store_to_json,
    board_dict,
    expected_status_change_board_dict,
):
    runner = CliRunner()
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["task:update", "done", "1"])

    assert result.exit_code == 0
    assert "done" in result.output
    mocked_store_to_json.assert_called_once_with(expected_status_change_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_clean_board_cli_command(
    mocked_read_from_json, mocked_store_to_json, board_dict, expected_empty_board_dict
):
    runner = CliRunner()
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["board:clean"], input="y\n")

    assert result.exit_code == 0
    mocked_store_to_json.assert_called_once_with(expected_empty_board_dict)


@patch("whattodo.cli.store_to_json")
@patch("whattodo.cli.read_from_json")
def test_remove_task_cli_command(
    mocked_read_from_json,
    mocked_store_to_json,
    board_dict,
    expected_removed_task_board_dict,
):
    runner = CliRunner()
    mocked_read_from_json.return_value = board_dict

    result = runner.invoke(app, ["task:remove", "1"], input="y\n")

    assert result.exit_code == 0
    mocked_store_to_json.assert_called_once_with(expected_removed_task_board_dict)


@pytest.mark.parametrize(
    "param_command",
    [
        (["task:update", "done", "0"]),
        (["board:count"]),
        (["board:clean"]),
        (["task:add", "some task"]),
    ],
)
@pytest.mark.parametrize(
    "param_board",
    [
        ({}),
        ([]),
        (),
    ],
)
@patch("whattodo.cli.read_from_json")
def test_commands_that_need_a_board_must_exit_early_when_no_board_exists(
    mocked_read_from_json, param_board, param_command
):
    runner = CliRunner()
    mocked_read_from_json.return_value = param_board

    result = runner.invoke(app, param_command)

    assert result.exit_code == 0
    assert "There are no created boards yet!" in result.output
