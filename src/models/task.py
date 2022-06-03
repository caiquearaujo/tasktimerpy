from typing import Union
from .record import Record


class Task(Record):
    def __init__(self, project_name: str, name: str):
        self.__project = project_name
        self.__name = name
        self.__epic = None
        self.__story = None
        self.__done = 0

    def apply(self, record: dict):
        super().apply(record)
        self.__epic = record.get("epic", self.__epic)
        self.__story = record.get("story", self.__story)
        self.__done = record.get("done", self.__done)

    def markAsDone(self):
        self.__done = 1

    def markAsUndone(self):
        self.__done = 1

    def isDone(self) -> bool:
        return self.__done == 1

    def name(self) -> Union[str, None]:
        return self.__name

    def changeName(self, name: str):
        self.__name = name

    def project(self) -> Union[str, None]:
        return self.__project

    def changeProject(self, project: str):
        self.__project = project

    def epic(self) -> Union[str, None]:
        return self.__epic

    def changeEpic(self, epic: str):
        self.__epic = epic

    def story(self) -> Union[str, None]:
        return self.__story

    def changeStory(self, story: str):
        self.__story = story

    def primaryKey(self) -> str:
        return "task_id"
