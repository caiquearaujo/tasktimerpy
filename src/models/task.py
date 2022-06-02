from typing import Union
from .story import Story


class Task(Story):
    def __init__(self, record: dict):
        super().__init__(record)
        self.__story = None
        self.__done = record.get("done", 0)

    def assignTo(self, story: Story):
        self.__story = story
        super().assignTo(story.epic())

    def done(self):
        self.__done = 1

    def isDone(self):
        return self.__done == 1

    def story(self) -> Union[Story, None]:
        return self.__story

    def primaryKey(self) -> str:
        return "task_id"
