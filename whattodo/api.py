"""Main API for whattodo project."""
from datetime import datetime
from typing import Dict
from typing import List
from typing import Type
from typing import TypedDict
from typing import TypeVar

T = TypeVar("T", bound="Task")
B = TypeVar("B", bound="Board")


TaskDict = TypedDict(
    "TaskDict",
    {"description": str, "status": bool, "created_at": str},
)

BoardDict = TypedDict(
    "BoardDict",
    {"name": str, "tasks": List[TaskDict], "created_at": str},
)


class Task:
    """
    Task representation that contains a description,
    status and creation date.
    """

    def __init__(self, description: str):
        """
        Task usage

            >>> task = Task("my first task")
            >>> task.description
            ... "my first task"
            >>> task.status
            ... ✘
            >>> task.status = "done"
            >>> task.status
            ... ކ
            >>> task.description = "updated description"
            >>> task.description
            ... updated description
        """
        self._description: str = description
        self._status: bool = False
        self._created_at: datetime = datetime.now()

    @property
    def description(self) -> str:
        """
        Retrieves the task description
        """
        return self._description

    @description.setter
    def description(self, updated_description: str) -> None:
        """
        Alters the task description

            >>> task.description = "new description"
            >>> task.description
            ... new description
        """
        self._description = updated_description

    @property
    def status(self) -> str:
        """
        Retrieves an unicode character representing the
        task status.
        """
        return "ކ" if self._status else "✘"

    @status.setter
    def status(self, updated_status: str) -> None:
        """
        Alters the task status.
        Use "done" to complete a task
        and "not done" to set the task
        as incomplete.

            >>> task.status = "done"
            >>> task.status
            ... ކ
            >>> task.status = "not done"
            ... ✘
        """
        if updated_status == "done":
            self._status = True
        elif updated_status == "not done":
            self._status = False

    @property
    def created_at(self) -> str:
        """
        Retrieves the creation date of a task.

            >>> task.created_at
            ... 2020-12-25 00:00:00
        """
        return self._created_at.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls: Type[T], dict_task) -> T:
        """
        Returns a board object created from a dict.
        """
        task = cls(
            description=dict_task["description"]
        )  # pylint: disable=protected-access
        task._status = dict_task["status"]  # pylint: disable=protected-access
        task._created_at = datetime.strptime(  # pylint: disable=protected-access
            dict_task["created_at"], "%Y-%m-%d %H:%M:%S"
        )
        return task

    def to_dict(self) -> Dict:
        """
        Parses the board to a dict.
        """
        return {
            "description": self._description,
            "status": self._status,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        return f"{self._description} {self.status}"

    def __repr__(self) -> str:
        return f"<Task {self._description} >"


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
    def name(self):
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

    def retrieve_task(self, index: int) -> Task:
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

    def to_dict(self) -> Dict:
        """
        Parses the board to a dict.
        """
        parsed_tasks = [task.to_dict() for task in self.tasks] if self.tasks else []
        return {"name": self.name, "tasks": parsed_tasks}

    def __repr__(self) -> str:
        return f"<Board {self._name} >"

    def __str__(self) -> str:
        return self.list_tasks
