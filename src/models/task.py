from typing import Union
from slugify import slugify
from .record import Record


class Task(Record):
    def __init__(self, project_name: str, name: str):
        super().__init__()
        self.__project = slugify(project_name)
        self.__name = name
        self.__epic = None
        self.__story = None
        self.__done = 0

    def apply(self, record: dict):
        self.__done = record.get("done", self.__done)

        epic = record.get("epic", self.__epic)
        story = record.get("story", self.__story)

        if epic is not None:
            self.changeEpic(epic)

        if story is not None:
            self.changeStory(story)

        super().apply(record)
        return self

    def markAsDone(self):
        self.__done = 1
        return self

    def markAsUndone(self):
        self.__done = 0
        return self

    def isDone(self) -> bool:
        return self.__done == 1

    def name(self) -> Union[str, None]:
        return self.__name

    def changeName(self, name: str):
        self.__name = name
        return self

    def project(self) -> Union[str, None]:
        return self.__project

    def changeProject(self, project: str):
        self.__project = slugify(project)
        return self

    def epic(self) -> Union[str, None]:
        return self.__epic

    def changeEpic(self, epic: str):
        self.__epic = slugify(epic)
        return self

    def story(self) -> Union[str, None]:
        return self.__story

    def changeStory(self, story: str):
        self.__story = slugify(story)
        return self

    def primaryKey(self) -> str:
        return "task_id"

    def toDict(self) -> dict:
        return {
            "id": self.id(),
            "project": self.__project,
            "epic": self.__epic,
            "story": self.__story,
            "name": self.__name,
            "done": self.__done,
            "createdAt": self.createdAt(),
        }
