"""CLI for whattodo project."""

import typer

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
    if state["verbose"]:
        typer.echo("Just created the board {board_name}")


@app.command("task:add")
def add_task(description: str):
    """
    Creates a new task with a DESCRIPTION to an active board.
    """
    if state["verbose"]:
        typer.echo("About to add a new task to board")
    typer.echo(
        f"Creating a task with description {description} to board {state['board']}"
    )
    if state["verbose"]:
        typer.echo("Just created the task {description}")


@app.command("task:update")
def update_task(status: str):
    """
    Updates task with to the given STATUS.
    """
    typer.echo(f"Updating the task to status {status}")


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
