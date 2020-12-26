"""Board API for whattodo project."""

from typing import List
from typing import Type
from typing import TypedDict
from typing import TypeVar

from whattodo.api.task import Task
from whattodo.api.task import TaskDict

B = TypeVar("B", bound="Board")

BoardDict = TypedDict(
    "BoardDict",
    {"name": str, "tasks": List[TaskDict]},
)


class Board:
    """
    Board representation that will hold tasks.
    """

    def __init__(self, name):
        """
        >>> board = Board(name="Personal")
        >>> board.add(first_task)
        >>> board.list_tasks
        ... =============================================================================
        ... Personal
        ... =============================================================================
        ... my first task                                    ✘        2020-12-25 00:00:00
        """
        self._name = name
        self._tasks: List[Task] = []

    @property
    def name(self) -> str:
        """
        Retrieved the board name.
        """
        return self._name

    @property
    def tasks(self):
        """
        Retrieves the tasks repository.
        """
        return self._tasks

    def add(self, task: Task):
        """
        Adds a Task object to the board.
        """
        self._tasks.append(task)

    @property
    def list_tasks(self) -> str:
        """
        Lists all tasks in a string representation.
        """
        task_representation = ""
        if not self._tasks:
            return f"""
            =============================================================================\n
            {self._name}\n
            =============================================================================\n
            No tasks on this board!
            """
        for task in self._tasks:
            task_representation += f"""
            {task.description}                                    {task.status}        {task.created_at}\n
            """
        return f"""
        =============================================================================\n
        {self._name}\n
        =============================================================================\n
        {task_representation}
        """

    @property
    def count_tasks(self) -> int:
        """
        Counts the number of tasks.
        """
        return len(self._tasks)

    def retrieve_task(self, index: int):
        """
        Retrieves a task given it's 0 based index.

        @raises ValueError: When no tasks are present on the board.

        @raises IdexError: When the given index doesn't have a task.
        """

        if not self._tasks:
            raise ValueError("No tasks on this board!")
        try:
            return self._tasks[index]
        except IndexError as excinfo:
            raise IndexError(f"No tasks found at the index {index}") from excinfo

    @classmethod
    def from_dict(cls: Type[B], dict_board) -> B:
        """
        Returns a board object created from a dict.
        """
        board = cls(name=dict_board["name"])
        board._tasks = [  # pylint: disable=protected-access
            Task.from_dict(dict_task) for dict_task in dict_board["tasks"]
        ]
        return board

    def to_dict(self) -> BoardDict:
        """
        Parses the board to a dict.
        """
        parsed_tasks = [task.to_dict() for task in self.tasks] if self.tasks else []
        return {"name": self.name, "tasks": parsed_tasks}

    def __repr__(self) -> str:
        return f"<Board {self._name} >"

    def __str__(self) -> str:
        return self.list_tasks
