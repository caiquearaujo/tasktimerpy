from typing import Union
from models.story import Story


class Task(Story):
    def __init__(self, record: dict):
        super().__init__(record)
        self.__story = None

    def assignTo(self, story: Story):
        self.__story = story
        super().assignTo(story.epic())

    def story(self) -> Union[Story, None]:
        return self.__story

    def primaryKey() -> str:
        return "task_id"
