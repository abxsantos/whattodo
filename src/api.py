from datetime import datetime


class Task(object):
    def __init__(self, description: str):
        self._description: str = description
        self._status: bool = False
        self._created_at: datetime = datetime.now()

    @property
    def description(self) -> str:
        return self._description

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def status(self) -> str:
        return "ކ" if self._status else "✘"

    @status.setter
    def status(self, updated_status: str) -> None:
        if updated_status == "done":
            self._status = True
        elif updated_status == "not done":
            self._status = False
