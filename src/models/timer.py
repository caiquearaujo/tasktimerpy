from typing import Union
from datetime import datetime
from .record import Record
from .task import Task


class Timer(Record):
    def __init__(self, record: dict = {}):
        super().__init__(record)
        self.__project = None
        self.__epic = None
        self.__story = None
        self.__task = None

        self.__starts_at = record.get(
            "starts_at", int(datetime.now().timestamp())
        )
        self.__ends_at = record.get("ends_at", None)
        self.__created_at = record.get(
            "created_at", int(datetime.now().timestamp())
        )

    def assignTo(self, task: Task):
        self.__task = task
        self.__story = task.story()
        self.__epic = task.epic()
        self.__project = task.project()

    def project(self):
        return self.__project

    def epic(self):
        return self.__epic

    def story(self):
        return self.__story

    def task(self):
        return self.__task

    def close(self):
        self.__ends_at = int(datetime.now().timestamp())

    def startsAt(self) -> int:
        return self.__starts_at

    def endsAt(self) -> Union[int, None]:
        return self.__ends_at

    def isDone(self) -> bool:
        return self.__ends_at != None

    def createdAt(self) -> int:
        return self.__created_at

    def primaryKey(self) -> str:
        return "timer_id"
