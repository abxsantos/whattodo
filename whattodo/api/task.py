"""Task API for whattodo project."""

from datetime import datetime
from typing import Type
from typing import TypedDict
from typing import TypeVar

T = TypeVar("T", bound="Task")

TaskDict = TypedDict(
    "TaskDict",
    {"description": str, "status": bool, "created_at": str},
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

    def to_dict(self) -> TaskDict:
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
