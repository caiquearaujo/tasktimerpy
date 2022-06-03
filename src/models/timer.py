from typing import Union
from datetime import datetime
from .record import Record
from .task import Task


class Timer(Record):
    def __init__(self):
        super().__init__()
        self.__task = None
        self.__starts_at = int(datetime.now().timestamp())
        self.__ends_at = None

    def apply(self, record: dict):
        self.__starts_at = record.get("starts_at", self.__starts_at)
        self.__ends_at = record.get("ends_at", self.__ends_at)
        super().apply(record)

    def assignTo(self, task: Task):
        self.__task = task
        return self

    def project(self) -> Union[str, None]:
        if self.__task is None:
            return None

        return self.__task.project()

    def epic(self) -> Union[str, None]:
        if self.__task is None:
            return None

        return self.__task.epic()

    def story(self) -> Union[str, None]:
        if self.__task is None:
            return None

        return self.__task.story()

    def task(self) -> Union[Task, None]:
        return self.__task

    def close(self):
        self.__ends_at = int(datetime.now().timestamp())
        return self

    def startsAt(self) -> int:
        return self.__starts_at

    def endsAt(self) -> Union[int, None]:
        return self.__ends_at

    def isDone(self) -> bool:
        return self.__ends_at != None

    def primaryKey(self) -> str:
        return "timer_id"

    def toDict(self) -> dict:
        return {
            "id": self.id(),
            "task": self.__task.toDict()
            if self.__task is not None
            else None,
            "startsAt": self.__starts_at,
            "endsAt": self.__ends_at,
            "createdAt": self.createdAt(),
        }
