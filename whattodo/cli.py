"""CLI for whattodo project."""

import typer

from whattodo.api.board import Board
from whattodo.api.task import Task
from whattodo.file_storage import read_from_json
from whattodo.file_storage import store_to_json

app = typer.Typer(help="WhatTodo CLI manager.")
state = {"verbose": False}


@app.command("board:add")
def add_board(board_name: str):
    """
    Creates a new Board with BOARD_NAME to hold tasks.
    """
    if state["verbose"]:
        typer.echo("About to create a board with name {board_name}")
    typer.echo(f"Creating a board with name {board_name}")
    board = Board(name=board_name)
    store_to_json(data=board.to_dict())
    if state["verbose"]:
        typer.echo("Just created the board {board_name}")


@app.command("board:list")
def list_tasks():
    """
    Lists all tasks in the current active board.
    """
    storage_data = read_from_json()
    if not storage_data:
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        board = Board.from_dict(storage_data)
        typer.echo(board.list_tasks)


@app.command("board:count")
def count_tasks():
    """
    Counts all tasks in the current active board.
    """
    storage_data = read_from_json()
    if not storage_data:
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        board = Board.from_dict(storage_data)
        typer.echo(f"The board '{board.name}' currently have {board.count_tasks} tasks")


@app.command("board:clean")
def clean_board():
    """
    Removes all tasks in the current active board.
    """
    storage_data = read_from_json()
    if not storage_data or not storage_data.get("tasks"):
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        typer.confirm(
            f"Are you sure you want to remove all tasks from the Board {storage_data['name']}?",
            abort=True,
        )
        board = Board.from_dict(storage_data)
        board.clean_tasks()
        store_to_json(board.to_dict())
        typer.echo(f"The board '{board.name}' was cleaned!")


@app.command("task:add")
def add_task(description: str):
    """
    Creates a new task with a DESCRIPTION to an active board.
    """
    storage_data = read_from_json()
    if not storage_data:
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        if state["verbose"]:
            typer.echo("About to add a new task to board")
        board = Board.from_dict(storage_data)
        typer.echo(f"Creating a task with description {description} to board")
        task = Task(description=description)
        board.add(task)
        store_to_json(board.to_dict())
        if state["verbose"]:
            typer.echo("Just created the task {description}")


@app.command("task:update")
def update_task(status: str, index: int):
    """
    Updates task with to the given STATUS.
    """
    storage_data = read_from_json()
    if not storage_data:
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        board = Board.from_dict(storage_data)
        task = board.retrieve_task(index)
        typer.echo(f"Updating the task to status {status}")
        task.status = status
        store_to_json(board.to_dict())


@app.command("task:remove")
def remove_task(index: int):
    """
    Removes a task based on it's 0 based index.
    """
    storage_data = read_from_json()
    if not storage_data:
        typer.echo("There are no created boards yet!")
        typer.Abort()
    else:
        typer.confirm(f"Are you sure you want to remove the task {index}?", abort=True)
        board = Board.from_dict(storage_data)
        board.remove_task(index)
        typer.echo(f"The task {index} was removed!")
        store_to_json(board.to_dict())


@app.callback()
def main(verbose: bool = False):
    """
    Manage Tasks in the awesome CLI app.
    """
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()
