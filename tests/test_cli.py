import pytest

from typer.testing import CliRunner

from whattodo.cli import app


@pytest.mark.smoke
def test_whattodo_cli_entrypoint():
    runner = CliRunner()
    result = runner.invoke(app, [])

    assert result.exit_code == 0

    assert "WhatTodo" in result.output


@pytest.mark.smoke
def test_add_board_cli_command():
    runner = CliRunner()
    board_name = "personal"

    result = runner.invoke(app, ["board:add", board_name])

    assert result.exit_code == 0
    assert board_name in result.output


@pytest.mark.smoke
def test_add_task_cli_command():
    runner = CliRunner()
    task_description = "my first task"

    result = runner.invoke(app, ["task:add", task_description])

    assert result.exit_code == 0
    assert task_description in result.output


@pytest.mark.smoke
def test_update_task_cli_command():
    runner = CliRunner()
    status = "done"

    result = runner.invoke(app, ["task:update", status])

    assert result.exit_code == 0
    assert status in result.output
