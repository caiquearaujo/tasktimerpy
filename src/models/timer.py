from typing import Union
from datetime import datetime
from .record import Record
from .task import Task


class Timer(Record):
    def __init__(self):
        self.__task = None
        self.__starts_at = int(datetime.now().timestamp())
        self.__ends_at = None

    def apply(self, record: dict):
        self.__starts_at = record.get("starts_at", self.__starts_at)
        self.__ends_at = record.get("ends_at", self.__ends_at)

    def assignTo(self, task: Task):
        self.__task = task

    def project(self) -> Union[str, None]:
        return self.__task.project() or None

    def epic(self) -> Union[str, None]:
        return self.__task.epic() or None

    def story(self) -> Union[str, None]:
        return self.__task.story() or None

    def task(self) -> Union[Task, None]:
        return self.__task

    def close(self):
        self.__ends_at = int(datetime.now().timestamp())

    def startsAt(self) -> int:
        return self.__starts_at

    def endsAt(self) -> Union[int, None]:
        return self.__ends_at

    def isDone(self) -> bool:
        return self.__ends_at != None

    def primaryKey(self) -> str:
        return "timer_id"
